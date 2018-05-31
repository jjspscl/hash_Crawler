# PACKAGES
import requests
import unicodedata
from bs4 import BeautifulSoup
from pprint import pprint
import re

# URL
url = 'https://www.symantec.com/connect/articles/petya-ransomware-next-global-threat'

# Save the web_response from request
r = requests.get(url)

# Extract the response as html: html_doc
html_doc = r.text

# Creating HTML object for Parsing
soup = BeautifulSoup(html_doc,"html.parser")
[x.extract() for x in soup.findAll('script')]

text = soup.get_text()
text = unicodedata.normalize('NFKD', text).encode('ascii','ignore').replace("\0"," ").replace("\t"," ").replace("\r"," ")#.split("\n")

# WRITE THE DOCUMENT TO A READABLE TEXT FILE
#with open("out.txt", "wb") as f:
#    f.write(text)

#pprint(text)

# FIND HASHES with REGEX
md5 = re.findall(r"\b[0-9a-fA-F]{32}\b",text) #MD5
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
