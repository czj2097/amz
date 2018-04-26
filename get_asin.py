import time
import urllib2
import urllib
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent' : ua.random}
#ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
#headers = {'User-Agent' : ua}
addr = 'https://www.amazon.com/gp/new-releases/hi/511228/'
req = urllib2.Request(addr,headers=headers)

response = urllib2.urlopen(req)
raw_html = response.read()
bsObj = BeautifulSoup(raw_html,'html.parser')
req_num = 1
#while re.search(r'New Releases in.*?Previous page',raw_html,re.S)==None and req_num<20:
while bsObj.find("div",id="zg-center-div")==None and req_num<20:
	time.sleep(10)
	response = urllib2.urlopen(req)
	raw_html = response.read()
	bsObj = BeautifulSoup(raw_html,'html.parser')
	req_num = req_num+1
if req_num == 20:
	print("Error: url request 20 times, still get the wrong page, please check")
	#target_area = re.search(r'New Releases in.*?New Releases in',raw_html,re.S).group()
	target_area = bsObj.find("div",id="zg_centerListWrapper")
else:
	print("Request times: "+str(req_num))
	#target_area = re.search(r'New Releases in.*?Previous page',raw_html,re.S).group()
	target_area = bsObj.find("div",id="zg-center-div")

pattern_9 = re.compile(r'/B0......./',re.S)
pattern_10 = re.compile(r'/B0......../',re.S)
pattern_11 = re.compile(r'/B0........./',re.S)
result_9 = pattern_9.findall(str(target_area))
result_10 = pattern_10.findall(str(target_area))
result_11 = pattern_11.findall(str(target_area))
newResult = []
for ele1 in result_9:
	if ele1 not in newResult:
		newResult.append(ele1)
for ele2 in result_10:
	if ele2 not in newResult:
		newResult.append(ele2)
for ele3 in result_11:
	if ele3 not in newResult:
		newResult.append(ele3)

#bsObj = BeautifulSoup(html,'html.parser')
#t2=bsObj.find_all("table")
#t1=bsObj.find_all("table",id="productDetails_detailBullets_sections1")
#t2=bsObj.table
#print t1
#print t2
#for t2 in t1:
#	t3=t2.get('href')
#	print(t3)

print(newResult)
print("ASIN number: "+str(len(newResult)))
