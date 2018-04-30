import time
import urllib2
import re
import xlwt
from bs4 import BeautifulSoup

from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent' : ua.random}
#ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
#headers = {'User-Agent' : ua}

def get_ASIN(addr):
	newResult = []
	k=0
	while True:
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
			print("Next page not exist! Get "+str(k+1)+" pages in all.")
			break;
		else:
			addr=next_page
			k=k+1
	
	return newResult


page = 'https://www.amazon.com/gp/new-releases/hi/511228/'
ASINs = get_ASIN(page)

wbk = xlwt.Workbook()
sheet_1 = wbk.add_sheet('AllASIN')
for i in range(0,len(ASINs)):
	sheet_1.write(i,0,ASINs[i])
sheet_1.write(0,1,0)
sheet_1.write(1,1,len(ASINs))
sheet_1.write(2,1,0)
sheet_1.write(3,1,0)


Titles = ["ASIN","Review","Stars","Rank1","RankDetail1","Rank2","RankDetail2","Rank3","RankDetail3","Date"]
sheet_2 = wbk.add_sheet('ProductDetails')
for j in range(0,len(Titles)):
	sheet_2.write(0,j,Titles[j])

sheet_3 = wbk.add_sheet('ErrorASIN')
wbk.save('ProductDetails.xls')
