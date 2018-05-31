""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                            INITIALIZATION
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys, os, re, unicodedata, json
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from pyvirtualdisplay import Display
from ConfigParser import RawConfigParser as config

# CHROME DRIVER INIT
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--log-level=3")
options.add_argument('--disable-extensions')
driver = webdriver.Chrome(chrome_options=options)

path = os.path.dirname(sys.argv[0]) # PATH

# JSON WRITER
dict =  {
        "SOURCE": "",
        "MD5": "",
        "SHA256": "",
        "SHA1": "",
        }

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                                FUNCTIONS
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def req(link): #
    driver.get(link)
    doc = driver.page_source # EXTRACT LOAD CONTENT

    return doc

def bsoup(doc):
    soup = BeautifulSoup(doc,"html.parser")
    [x.extract() for x in soup.findAll('script')]

    return soup

def soup_text(soups):
    text = soups.get_text()
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore').replace("\0"," ").replace("\t"," ")#.replace("\n"," ").replace("\r"," ")

    return text

def hash(contents):
    all_hash = []

    # FIND HASHES with REGEX
    md5 = re.findall(r"\b(?!^[\s\d]*$)[0-9a-fA-F]{32}\b",contents) #MD5
    #md5 = re.findall(r"\b(?!^[\d]*$)(?!^[a-fA-F]*$)([a-f\d]{32}|[A-F\d]{32})\b",text) #MD5
    md5 = list(set(md5))
    all_hash.append(md5)

    sha256 = re.findall(r"\b[A-Fa-f0-9]{64}\b",contents) #SHA256
    sha256 = list(set(sha256))
    all_hash.append(sha256)

    sha1 = re.findall(r"\b[0-9a-f]{40}\b",contents) #sh
    sha1 = list(set(sha1))
    all_hash.append(sha1)

    return all_hash

def writer(link,writes):
    global dict
    dict = dict.fromkeys(dict, "")  #CLEAR DICTIONARY WRITER

    dict['SOURCE'] = link
    for index,data in enumerate(writes):
        if index == 0:
            print("MD5")
            if data != []:
                dict['MD5'] = writes[0]
            else:
                dict['MD5'] = ""
        if index == 1:
            print("SHA256")
            if data != []:
                dict['SHA256'] = writes[1]
            else:
                dict['SHA256'] = ""
        if index == 2:
            print("SHA1")
            if data != []:
                dict['SHA1'] = writes[2]
            else:
                dict['SHA1'] = ""
    return dict

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                            MAIN PROGRAM
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def main():
    new_dict = []

    with open("%s\\config.txt" % (path), "rb") as f: # READ TEXT FILES
        url = f.read().split("\r\n")
        url = filter(None, url)

    for link in url:
        print("PARSING: %s" % (link) )

        html_doc = req(link)
        soup = bsoup(html_doc)
        content = soup_text(soup)
        hashes = hash(content)
        write = writer(link,hashes)
        new_dict.append(write) #PASS THE UPDATE TO WRITER

    driver.close()

    with open("hashes", "wb") as w: #THROW PARSED TO JSON FILE
       json.dump(new_dict, w, indent = 4)

if __name__ == "__main__": #EXECUTION POINT
    main()
