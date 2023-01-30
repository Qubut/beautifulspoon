from functools import reduce
from bs4 import BeautifulSoup, Tag
from typing import List, Tuple, Dict, Union
import pandas as pd
from requests import get


def getPage(url: str) -> str:
    """Get the content of a web page given its url.
    
    Arguments:
        url {str} -- The url of the web page to retrieve.
    
    Returns:
        str -- The content of the web page.
    """
    return get(url).text


def get_tables(url: str) -> List[Tag]:
    """Get all the tables in a web page.
    
    Arguments:
        url {str} -- The url of the web page to retrieve.
    
    Returns:
        List[Tag] -- The list of tables in the web page.
    """
    return BeautifulSoup(getPage(url), 'lxml').find_all('table')


def exmaineThead(table: Tag) -> Tuple[Dict[str, List[Tuple[int, str]]], List[Tuple[int, str]]]:
    """Examine the header of a table.
    
    Arguments:
        table {Tag} -- The table to examine.
    
    Returns:
        Tuple[Dict[str, List[Tuple[int, str]]], List[Tuple[int, str]]] -- A tuple containing two elements:
            - A dictionary mapping group names to lists of column labels.
            - A list of single column labels.
    """
    # Get all header cells in the table.
    ths =  list(
        filter(
            lambda h: h.find('img') == None and h.find('p') == None, 
            table.find_all('th')
        )
    )
    
    # Define a function to check if a header cell belongs to a group.
    is_group = lambda tag: tag.has_attr(
        'colspan') and int(tag['colspan']) > 1
    
    # Get all group header cells.
    groups = list(filter(is_group, ths))
    
    # Get all single header cells.
    labels = enumerate(filter(lambda h: not is_group(h), ths))
    
    # Get the number of groups.
    num_of_groups = len(groups)
    dic = dict()
    single_labels = []
    
    if num_of_groups:
        def appender():
            """An inner function to append the next header cell
              to either the dictionary of group labels or the list of single labels."""
            label: Tuple[int, Tag] | None = next(labels, None)
            if(label):
                l = (label[0], label[1].get_text(strip=r'\s'))
                if(label[1].has_attr('rowspan')):
                    single_labels.append(l)
                    appender()
                else:
                    dic[gr_name].append(l)
            return
        for group in groups:
            gr_name = group.get_text(strip=r'\s')
            dic[gr_name] = []
            num_of_elements = int(group['colspan'])
            for _ in range(num_of_elements):
                appender()
        return (dic, single_labels)
    else:
        return (dict(), [(label[0], label[1].get_text(strip=r'\s')) for label in labels])


def get_rows(table: Tag) -> List[Tag]:
    """Get all the rows in a table.
    
    Arguments:
        table {Tag} -- The table to retrieve the rows from.
    
    Returns:
        List[Tag] -- The list of rows in the table.
    """
    return table.find_all('tr')


def create_dfs(table:Tag) -> Union[Dict[str,pd.DataFrame],pd.DataFrame]:
    """Create one or more pandas dataframes from a table.
    
    Arguments:
        table {Tag} -- The table to create the dataframes from.
    
    Returns:
        Union[Dict[str,pd.DataFrame],pd.DataFrame] -- If the header of the table contains 
        multiple groups of columns, then a dictionary of dataframes is returned, 
        otherwise, a single dataframe is returned. The keys of the dictionary represent the 
        names of the column groups, and the values are the corresponding dataframes.
    """
    groups, individuals = exmaineThead(table)
    dfs_dic: Dict[str,pd.DataFrame] = {}
    single_col_dfs: List[pd.DataFrame] = []
    def fill_dfs(item: Tuple[str,List[Tuple[int,str]]]|Tuple[int,str]):
        """Inner function that fills the dataframes with the data from the table.
        
        Arguments:
            item {Iterable} -- An iterable of column labels.
        
        """
        nonlocal dfs_dic
        nonlocal single_col_dfs
        if isinstance(item[1], List):
            if len(item[1])>1:
                dfs_dic[item[0]] = pd.DataFrame(
                columns=[f"{col[1]}:{col[0]}" for col in item[1]])
            else:
                single_col_dfs.append(pd.DataFrame(columns=[f"{item[0]}:{item[1][0][0]}"]))
        else:
            single_col_dfs.append(pd.DataFrame(columns=[f"{item[1]}:{item[0]}"]))
    def filler(ds:Tuple[str,pd.DataFrame]|pd.DataFrame)->Tuple[str,pd.DataFrame]|pd.DataFrame:
            df = ds[1] if isinstance(ds,Tuple) else ds
            indices = (int(cl[-1]) for cl in df.columns)
            selection = [data[i] for i in indices]
            df.loc[df.shape[0]] = selection
            return (ds[0],df) if isinstance(ds,Tuple) else df
    clean = lambda strings:[s[:-2] for s in strings]
    for group in groups.items():
        fill_dfs(group)
    for individual in individuals:
        fill_dfs(individual)
    for row in get_rows(table):
        data = [c.get_text(strip=r'\s') for c in row.find_all('td')]
        if data:
            dfs_dic = dict(map(filler,dfs_dic.items()))
            single_col_dfs = list(map(filler,single_col_dfs))
            
    if not groups: 
        df = pd.concat(single_col_dfs,axis=1)
        df.columns = clean(df.columns)
        return df
    elif individuals and groups:
        for df in dfs_dic.items():
            for s in single_col_dfs:
                df[1][s.columns[0]]=s[s.columns[0]].values
            df[1].columns = [col[:-2] for col in df[1].columns]
    else:
        return dfs_dic
