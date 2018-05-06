import urllib2
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

#ua = UserAgent()
#headers = {'User-Agent' : ua.random}
ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
headers = {'User-Agent' : ua}

addr = 'https://www.amazon.com/dp/B07BR4NM77/'

req = urllib2.Request(addr,headers=headers)
response = urllib2.urlopen(req)
raw_html = response.read()
bsObj = BeautifulSoup(raw_html,'html.parser')
if bsObj.find("table",id="productDetails_detailBullets_sections1")!=None:
	html = bsObj.find("table",id="productDetails_detailBullets_sections1")
else:
	if bsObj.find("table",cellpadding=True,cellspacing=True)!=None:
		html = bsObj.find("table",cellpadding=True,cellspacing=True)
	else:
		print("Error: Both tables not found! Save the whole page")
		html = raw_html

fh = open('amazon_origin.html','w')
fh.write(str(html))
fh.close()

