""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                            INITIALIZATION
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys, os, re, unicodedata, json, threading,time
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from pyvirtualdisplay import Display
from ConfigParser import RawConfigParser as config

path = os.path.dirname(sys.argv[0])

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--log-level=3")  # fatal
options.add_argument('--disable-extensions')
driver = webdriver.Chrome('%s//chromedriver' % (path),chrome_options=options)

dict =  {
        "SOURCE": "",
        "MD5": "",
        "SHA256": "",
        "SHA1": "",
        }

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                                FUNCTIONS
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)

def clear(): # CLEAR SCREEN FUNCTION
    os.system('cls' if os.name == 'nt' else 'clear')

def req(link):
    spinner = Spinner()

    spinner.start()

    driver.get(link)
    doc = driver.page_source # Extract loaded content

    spinner.stop()
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
    md5 = re.findall(r"\s(?!^[\d]*$)(?!^[a-fA-F]*$)([a-f\]{32}|[A-F\d]{32})\b",contents) #MD5
    md5 = list(set(md5))
    md5 = [x.strip() for x in md5]
    all_hash.append(md5)

    sha256 = re.findall(r"\s[A-Fa-f0-9]{64}\b",contents) #SHA256
    sha256 = list(set(sha256))
    sha256 = [x.strip() for x in sha256]
    all_hash.append(sha256)

    sha1 = re.findall(r"\s[0-9a-f]{40}\b",contents) #sh
    sha1 = list(set(sha1))
    sha1 = [x.strip() for x in sha1]
    all_hash.append(sha1)

    return all_hash

def writer(link,writes):
    global dict
    dict = dict.fromkeys(dict, "")  #CLEAR DICTIONARY WRITER

    dict['SOURCE'] = link
    for index,data in enumerate(writes):
        if index == 0:
            if data != []:
                dict['MD5'] = writes[0]
            else:
                dict['MD5'] = ""
        if index == 1:
            if data != []:
                dict['SHA256'] = writes[1]
            else:
                dict['SHA256'] = ""
        if index == 2:

            if data != []:
                dict['SHA1'] = writes[2]
            else:
                dict['SHA1'] = ""
    print("SHA1: %i  SHA256: %i  MD5: %i\n" % (len(writes[2]),len(writes[1]),len(writes[0])))
    return dict

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#                            MAIN PROGRAM
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def main():
    new_dict = []

    clear()

    with open("%s\\config.txt" % (path), "rb") as f:
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

    with open("hashes.json", "wb") as write_file: #THROW PARSED TO JSON FILE
       json.dump(new_dict, write_file, indent = 4)

if __name__ == "__main__": #EXECUTION POINT
    main()
