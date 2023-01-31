from itertools import zip_longest
import numpy as np
from bs4 import BeautifulSoup, Tag
from typing import List, Tuple, Iterable, Dict
import pandas as pd
from requests import get

def getPage(url): return get(url).text

def get_tables(url: str) -> List[Tag]:
    return BeautifulSoup(getPage(url), 'lxml').find_all('table')


def exmaineThead(table: Tag) -> Tuple[Dict[str, List[Tuple[int, str]]], List[Tuple[int, str]]]:
    ths =  list(
        filter(
            lambda h: h.find('img') == None and h.find('p') == None, 
            table.find_all('th')
            )
        )
    isGroup = lambda tag: tag.has_attr(
        'colspan') and int(tag['colspan']) > 1
    groups = list(filter(isGroup, ths))
    labels = enumerate(filter(lambda h: not isGroup(h), ths))
    num_of_groups = len(groups)
    dic = dict()
    single_labels = []
    if num_of_groups:
        def appender():
            label: Tuple[int, Tag] | None = next(labels, None)
            if(label):
                l = (label[0], label[1].get_text(strip="\s"))
                if(label[1].has_attr('rowspan')):
                    single_labels.append(l)
                    appender()
                else:
                    dic[gr_name].append(l)
            return
        for group in groups:
            gr_name = group.get_text(strip='\s')
            dic[gr_name] = []
            num_of_elements = int(group['colspan'])
            for _ in range(num_of_elements):
                appender()
        return (dic, single_labels)
    else:
        return (dict(), [(label[0], label[1].get_text(strip="\s")) for label in labels])


def get_rows(table: Tag):
    return table.find_all('tr')



def create_dfs(table:Tag) -> List[pd.DataFrame]|pd.DataFrame:
    groups, individuals = exmaineThead(table)
    dataframes: List[pd.DataFrame] = []
    
    def fill_dfs(it: Iterable):
        if not isinstance(it, Tuple):
            dataframes.append(pd.DataFrame(
            columns=[f"{col[1]}:{col[0]}" for col in it]))
        else:
            dataframes.append(pd.DataFrame(columns=[f"{it[1]}:{it[0]}"]))
    for group in groups.values():
        fill_dfs(group)
    for individual in individuals:
        fill_dfs(individual)
    for row in get_rows(table):
        data = [c.get_text(strip='\s') for c in row.find_all('td')]
        if data:
            for df in dataframes:
                indices = (int(cl[-1]) for cl in df.columns)
                selection = [data[i] for i in indices]
                df.loc[df.shape[0]] = selection
    for df in dataframes:
        df.columns = [col[:-2] for col in df.columns]
    if not groups: 
        return pd.concat(dataframes)
    return dataframes

link1 = 'https://www.boxofficemojo.com/weekend/by-year/2021/?area=DE'
link2 = 'https://en.wikipedia.org/wiki/List_of_extreme_temperatures_in_Germany'
link3 =  'https://en.wikipedia.org/wiki/Germany'
tables = get_tables(link3)

dataframes = create_dfs(tables[2])
print(dataframes)
# print(tables[2])
# print(create_dfs(tables[1]))
