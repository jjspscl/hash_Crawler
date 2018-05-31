# PACKAGES
import unicodedata
from bs4 import BeautifulSoup
from pprint import pprint
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Specify url: url
url = 'https://www.symantec.com/connect/articles/petya-ransomware-next-global-threat'

# Simulate browser loading ALL contents
driver = webdriver.Chrome()
driver.get(url)

html_doc = driver.page_source # Extract loaded content

# Create a BeautifulSoup object from the HTML: soup
soup = BeautifulSoup(html_doc,"html.parser")
[x.extract() for x in soup.findAll('script')]

text = soup.get_text()
text = unicodedata.normalize('NFKD', text).encode('ascii','ignore').replace("\0"," ").replace("\t"," ").replace("\r"," ")#.split("\n")

# WRITE THE DOCUMENT TO A READABLE TEXT FILE
#with open("out.txt", "wb") as f:
#    f.write(text)

#pprint(text)

driver.quit()


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
