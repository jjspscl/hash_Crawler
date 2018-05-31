""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                            INITIALIZATION
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import unicodedata
from bs4 import BeautifulSoup
from pprint import pprint
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from ConfigParser import RawConfigParser as config

with open("config.txt", "rb") as f:
    url = f.read().split("\r\n")

"""
# FIND HASHES with REGEX
md5 = re.findall(r"\b(?!^[\s\d]*$)[0-9a-fA-F]{32}\b",text) #MD5
#md5 = re.findall(r"\b(?!^[\d]*$)(?!^[a-fA-F]*$)([a-f\d]{32}|[A-F\d]{32})\b",text) #MD5
md5 = list(set(md5))

sha256 = re.findall(r"\b[A-Fa-f0-9]{64}\b",text) #SHA256
sha256 = list(set(sha256))

sha1 = re.findall(r"\b[0-9a-f]{40}\b",text) #sh
sha1 = list(set(sha1))

pprint(md5)
print(len(md5))

pprint(sha256)
print(len(sha256))

pprint(sha1)
print(len(sha1))

"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                                FUNCTIONS
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def req(link):
    driver = webdriver.Chrome()
    driver.get(url)

    doc = driver.page_source # Extract loaded content

    return doc

def bsoup(doc):
    soup = BeautifulSoup(doc,"html.parser")
    return soup

def soup_text(soups):
    text = soups.get_text()
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
           .replace("\0"," ").replace("\n"," ").replace("\r"," ")
           .replace("\t"," ")
    return text

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                            MAIN PROGRAM
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
    for link in url:
        html_doc = req(link).text
        soup = bsoup(html_doc)
        content = soup_text(soup)

if __name__ == "__main__": #EXECUTION POINT
    main()
