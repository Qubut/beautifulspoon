from bs4 import BeautifulSoup, Tag
from typing import List, Tuple, Dict, Union
import pandas as pd
from requests import get

<<<<<<< HEAD

=======
>>>>>>> datascience_ii
def get_tables(url: str) -> List[Tag]:
    """Get all the tables in a web page.
    
    Arguments:
        url {str} -- The url of the web page to retrieve.
    
    Returns:
        List[Tag] -- The list of tables in the web page.
    """
    response = get(url).text
    return BeautifulSoup(response, 'lxml').find_all('table')


<<<<<<< HEAD
def examine_thead(table: Tag) -> Tuple[Dict[str, List[Tuple[int, str]]], List[Tuple[int, str]]]:
=======
def exmaineThead(table: Tag) -> Tuple[Dict[str, List[Tuple[int, str]]], List[Tuple[int, str]]]:
>>>>>>> datascience_ii
    """Examine the header of a table.
    
    Arguments:
        table {Tag} -- The table to examine.
    
    Returns:
        Tuple[Dict[str, List[Tuple[int, str]]], List[Tuple[int, str]]] -- A tuple containing two elements:
            - A dictionary mapping group names to lists of column labels.
            - A list of single column labels.
    """
    # Get all header cells in the table.
<<<<<<< HEAD
    ths = [h for h in table.find_all('th')
           if not h.find('img') and not h.find('p')]

    # Define a function to check if a header cell belongs to a group.
    is_group = lambda tag: tag.has_attr(
        'colspan') and int(tag['colspan']) > 1

    # Get all group header cells.
    groups = list(filter(is_group, ths))

    # Get all single header cells.
    labels = enumerate((h for h in ths if not is_group(h)), 0)

=======
    ths =  [ h  for h in table.find_all('th')
            if h.find('img') == None and h.find('p') == None ]
    
    # Define a function to check if a header cell belongs to a group.
    is_group = lambda tag: tag.has_attr(
        'colspan') and int(tag['colspan']) > 1
    
    # Get all group header cells.
    groups = list(filter(is_group, ths))
    
    # Get all single header cells.
    labels = enumerate((h for h in ths if not is_group(h)),0)
    
>>>>>>> datascience_ii
    # Get the number of groups.
    num_of_groups = len(groups)
    dic = dict()
    single_labels = []
<<<<<<< HEAD

=======
    
>>>>>>> datascience_ii
    if num_of_groups:
        def appender():
            """An inner function to append the next header cell
              to either the dictionary of group labels or the list of single labels."""
            label: Tuple[int, Tag] | None = next(labels, None)
<<<<<<< HEAD
            if label:
                l = (label[0], label[1].get_text(strip=r'\s'))
                if label[1].has_attr('rowspan'):
=======
            if(label):
                l = (label[0], label[1].get_text(strip=r'\s'))
                if(label[1].has_attr('rowspan')):
>>>>>>> datascience_ii
                    single_labels.append(l)
                    appender()
                else:
                    dic[gr_name].append(l)
            return
<<<<<<< HEAD

=======
>>>>>>> datascience_ii
        for group in groups:
            gr_name = group.get_text(strip=r'\s')
            dic[gr_name] = []
            num_of_elements = int(group['colspan'])
            for _ in range(num_of_elements):
                appender()
<<<<<<< HEAD
        return dic, single_labels
    else:
        return dict(), [(label[0], label[1].get_text(strip=r'\s')) for label in labels]
=======
        return (dic, single_labels)
    else:
        return (dict(), [(label[0], label[1].get_text(strip=r'\s')) for label in labels])
>>>>>>> datascience_ii


def get_rows(table: Tag) -> List[Tag]:
    """Get all the rows in a table.
    
    Arguments:
        table {Tag} -- The table to retrieve the rows from.
    
    Returns:
        List[Tag] -- The list of rows in the table.
    """
    return table.find_all('tr')


<<<<<<< HEAD
def create_dfs(table: Tag) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
=======
def create_dfs(table:Tag) -> Union[Dict[str,pd.DataFrame],pd.DataFrame]:
>>>>>>> datascience_ii
    """Create one or more pandas dataframes from a table.
    
    Arguments:
        table {Tag} -- The table to create the dataframes from.
    
    Returns:
        Union[Dict[str,pd.DataFrame],pd.DataFrame] -- If the header of the table contains 
        multiple groups of columns, then a dictionary of dataframes is returned, 
        otherwise, a single dataframe is returned. The keys of the dictionary represent the 
        names of the column groups, and the values are the corresponding dataframes.
    """
<<<<<<< HEAD
    groups, individuals = examine_thead(table)
    dfs_dic: Dict[str, pd.DataFrame] = {}
    single_col_dfs: List[pd.DataFrame] = []

    def fill_dfs(item: Tuple[str, List[Tuple[int, str]]] | Tuple[int, str]):
=======
    groups, individuals = exmaineThead(table)
    dfs_dic: Dict[str,pd.DataFrame] = {}
    single_col_dfs: List[pd.DataFrame] = []
    def fill_dfs(item: Tuple[str,List[Tuple[int,str]]]|Tuple[int,str]):
>>>>>>> datascience_ii
        """Inner function that fills the dataframes with the data from the table.
        
        Arguments:
            item {Iterable} -- An iterable of column labels.
        
        """
        nonlocal dfs_dic
        nonlocal single_col_dfs
        if isinstance(item[1], List):
<<<<<<< HEAD
            if len(item[1]) > 1:
                dfs_dic[item[0]] = pd.DataFrame(
                    columns=[f"{col[1]}:{col[0]}" for col in item[1]])
=======
            if len(item[1])>1:
                dfs_dic[item[0]] = pd.DataFrame(
                columns=[f"{col[1]}:{col[0]}" for col in item[1]])
>>>>>>> datascience_ii
            else:
                single_col_dfs.append(pd.DataFrame(columns=[f"{item[0]}:{item[1][0][0]}"]))
        else:
            single_col_dfs.append(pd.DataFrame(columns=[f"{item[1]}:{item[0]}"]))
<<<<<<< HEAD

    def filler(ds: Tuple[str, pd.DataFrame] | pd.DataFrame) -> Tuple[str, pd.DataFrame] | pd.DataFrame:
        df = ds[1] if isinstance(ds, Tuple) else ds
        indices = (int(cl[-1]) for cl in df.columns)
        selection = [data[i] for i in indices]
        df.loc[df.shape[0]] = selection
        return (ds[0], df) if isinstance(ds, Tuple) else df
    clean = lambda strings: [string[:-2] for string in strings]
=======
    def filler(ds:Tuple[str,pd.DataFrame]|pd.DataFrame)->Tuple[str,pd.DataFrame]|pd.DataFrame:
            df = ds[1] if isinstance(ds,Tuple) else ds
            indices = (int(cl[-1]) for cl in df.columns)
            selection = [data[i] for i in indices]
            df.loc[df.shape[0]] = selection
            return (ds[0],df) if isinstance(ds,Tuple) else df
    clean = lambda strings:[s[:-2] for s in strings]
>>>>>>> datascience_ii
    for group in groups.items():
        fill_dfs(group)
    for individual in individuals:
        fill_dfs(individual)
    for row in get_rows(table):
        data = [c.get_text(strip=r'\s') for c in row.find_all('td')]
        if data:
<<<<<<< HEAD
            dfs_dic = dict(map(filler, dfs_dic.items()))
            single_col_dfs = list(map(filler, single_col_dfs))

    if not groups:
        df = pd.concat(single_col_dfs, axis=1)
=======
            dfs_dic = dict(map(filler,dfs_dic.items()))
            single_col_dfs = list(map(filler,single_col_dfs))
            
    if not groups: 
        df = pd.concat(single_col_dfs,axis=1)
>>>>>>> datascience_ii
        df.columns = clean(df.columns)
        return df
    elif individuals and groups:
        for df in dfs_dic.items():
            for s in single_col_dfs:
<<<<<<< HEAD
                df[1][s.columns[0]] = s[s.columns[0]].values
            df[1].columns = [col[:-2] for col in df[1].columns]
    return dfs_dic
=======
                df[1][s.columns[0]]=s[s.columns[0]].values
            df[1].columns = [col[:-2] for col in df[1].columns]
    else:
        return dfs_dic
>>>>>>> datascience_ii
