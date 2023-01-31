from bs4 import BeautifulSoup, Tag
from typing import List, Tuple, Dict, Union
import pandas as pd
from requests import get


def get_tables(url: str) -> List[Tag]:
    """Get all the tables in a web page.

    Arguments:
        url {str} -- The url of the web page to retrieve.

    Returns:
        List[Tag] -- The list of tables in the web page.
    """
    response = get(url).text
    return BeautifulSoup(response, 'lxml').find_all('table')


def examineThead(table: Tag) -> Tuple[Dict[str, List[Tuple[int, str]]], List[Tuple[int, str]]]:
    """Examine the header of a table.

    Arguments:
        table {Tag} -- The table to examine.

    Returns:
        Tuple[Dict[str, List[Tuple[int, str]]], List[Tuple[int, str]]] -- A tuple containing two elements:
            - A dictionary mapping group names to lists of column labels.
            - A list of single column labels.
    """
    # Get all header cells in the table.
    ths = [h for h in table.find_all('th')
           if h.find('img') == None and h.find('p') == None]

    # Define a function to check if a header cell belongs to a group.
    def is_group(tag): return tag.has_attr(
        'colspan') and int(tag['colspan']) > 1

    # Get all group header cells.
    groups = list(filter(is_group, ths))

    # Get all single header cells.
    labels = enumerate((h for h in ths if not is_group(h)), 0)

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


def create_dfs(table: Tag) -> pd.DataFrame:
    groups, individuals = examineThead(table)
    individual_items = [(None, [(None, individual)])
                        for individual in individuals]
    column_labels = list(groups.items()) + individual_items
    cols = [f"{col[1] if not isinstance(col[1],tuple) else col[1][1]}:{col[0] if col[0] else col[1][0]}" for _,
            cols in column_labels for col in cols]
    cols.sort(key=lambda a: int(a.split(':')[1]))
    columns = [c.split(':')[0] for c in cols]
    data = [l for l in [[c.get_text(strip=r'\s') for c in row.find_all('td')]
            for row in get_rows(table)] if l]
    df = pd.DataFrame(columns=columns, data=data)
    if not groups:
        return df
    return pd.concat([df.iloc[:, (val[0] for val in l)]for l in groups.values()], keys=groups.keys(), axis=1)

