import re
from bs4 import BeautifulSoup

with open('amazon_origin.html','r') as f:
	raw_html = f.read()
bsObj = BeautifulSoup(raw_html,'html.parser')

#all_tr = bsObj.find_all("tr")
#print(all_tr)
#print len(all_tr)

all_li = bsObj.find_all("li")
print(all_li)
print len(all_li)
