from bs4 import BeautifulSoup
from bs4.element import ResultSet
from pandas import Series
from numpy import array


def findAllImgs(html: str) -> ResultSet:
    return BeautifulSoup(html, "lxml").find_all("img")


def extractImgsUrls(imgs: ResultSet) -> Series:
    return Series(array([img.attrs["src"] for img in imgs]))


def extractImgsAlts(imgs: ResultSet) -> ResultSet:
    return Series(array([img.attrs["alt"] for img in imgs]))
