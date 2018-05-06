import time
import urllib2
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

#ua = UserAgent()
#headers = {'User-Agent' : ua.random}
ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
headers = {'User-Agent' : ua}
addr = 'https://www.amazon.com/gp/bestsellers/hi/3180261'

req = urllib2.Request(addr,headers=headers)
response = urllib2.urlopen(req)
raw_html = response.read()
req_num = 1
bsObj = BeautifulSoup(raw_html,'html.parser')
while bsObj.find("div",id="zg-center-div")==None and req_num<20:
	print("Get page of 20 items, try again")
	time.sleep(10)
        response = urllib2.urlopen(req)
        raw_html = response.read()
        bsObj = BeautifulSoup(raw_html,'html.parser')
	req_num = req_num + 1
if req_num == 20:
        print("Request 20 times, still get 20 items.")
        html = bsObj.find("div",id="zg_centerListWrapper")
else:
        print("Get 50 item page. Request times: "+str(req_num))
        html = bsObj.find("div",id="zg-center-div")

fh = open('amazon_origin.html','w')
fh.write(str(html))
fh.close()

