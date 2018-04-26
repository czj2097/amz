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
newResult = []
k=0

while k<2:
	req = urllib2.Request(addr,headers=headers)

	#Get page of 50 items, ignore page of 20 items
	response = urllib2.urlopen(req)
	raw_html = response.read()
	bsObj = BeautifulSoup(raw_html,'html.parser')
	req_num = 1
	while bsObj.find("div",id="zg-center-div")==None and req_num<20:
		time.sleep(10)
		response = urllib2.urlopen(req)
		raw_html = response.read()
		bsObj = BeautifulSoup(raw_html,'html.parser')
		req_num = req_num+1
	if req_num == 20:
		print("Error: url request 20 times, still get the wrong page, please check")
		targetObj = bsObj.find("div",id="zg_centerListWrapper")
	else:
		print("Request times: "+str(req_num))
		targetObj = bsObj.find("div",id="zg-center-div")

	#Get ASIN of current page
	pattern_9 = re.compile(r'/B0......./',re.S)
	pattern_10 = re.compile(r'/B0......../',re.S)
	pattern_11 = re.compile(r'/B0........./',re.S)
	result_9 = pattern_9.findall(str(targetObj))
	result_10 = pattern_10.findall(str(targetObj))
	result_11 = pattern_11.findall(str(targetObj))
	for ele1 in result_9:
		if ele1 not in newResult:
			newResult.append(ele1)
	for ele2 in result_10:
		if ele2 not in newResult:
			newResult.append(ele2)
	for ele3 in result_11:
		if ele3 not in newResult:
			newResult.append(ele3)

	#Get addr of next page
	next_page = addr
	all_a = targetObj.find_all("a")
	for i in all_a:
        	if i.find(text = "Next page") != None:
                	target_a = i
                	next_page = str(target_a.get('href'))
                	print("next_page addr="+next_page)
	if next_page == addr:
		print("next page not exist! Output ASIN of start page.")
		break;
	else:
		addr=next_page
		k=k+1

print(newResult)
print("ASIN number: "+str(len(newResult)))
