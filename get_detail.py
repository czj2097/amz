import urllib2
import re
from bs4 import BeautifulSoup

import time
import datetime

import xlwt
import xlrd
from xlutils.copy import copy

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent' : ua.random}

def get_detail_of_oneASIN(oneASIN):
	print("\nASIN:"+oneASIN)
	details = []
	errASIN = []
	review = 0
	star = 0.0
	rank = [0,0,0]
        category = ['0','0','0']
	date = '0000-00-00'

	addr = "https://www.amazon.com/dp"+oneASIN
	req = urllib2.Request(addr,headers=headers)
        response = urllib2.urlopen(req)
        raw_html = response.read()
	bsObj = BeautifulSoup(raw_html,'html.parser')
	table = bsObj.find("table",id="productDetails_detailBullets_sections1")
	if table == None:
		errASIN.append(oneASIN)
		print("Error: table not found, return errASIN")
		return errASIN
	else:
		all_tr = table.find_all("tr")
	for tr in all_tr:
		if tr.find("th") == None or tr.find("td") ==None:
			errASIN.append(oneASIN)
        	        print("Error: th or td not found, return errASIN")
	                return errASIN

		item = tr.find("th").string
		value = tr.find("td")

		if re.search(r'Customer Reviews',item):
			all_a = value.find_all("a")
			for a in all_a:
				rw_pattern1 = re.compile(r'([0-9,]*) customer reviews',re.I)
				rw_pattern2 = re.compile(r'([0-9\.]*) out of 5 stars',re.I)
				rw_target1 = rw_pattern1.search(str(a))
				rw_target2 = rw_pattern2.search(str(a))
				if rw_target1 != None:
					review = int(rw_target1.group(1).replace(',',''))
				if rw_target2 != None:
					star = float(rw_target2.group(1))
			print("Get review successfully")
			#print(review)
			#print(star)

		elif re.search(r'Best Sellers Rank',item):
			rk_k = 0
			all_span = value.span.find_all("span")
			for span in all_span:
				rk_pattern = re.compile(r'#([0-9,]*) in',re.I)
				rk_target = rk_pattern.search(str(span))
				if rk_target != None:
					rank[rk_k] = int(rk_target.group(1).replace(',',''))
					category[rk_k] = str(span.get_text())
				rk_k = rk_k+1
				if rk_k == 3:
					break;
			print("Get rank successfully")
			#print(rank)
			#print(category)

		elif re.search(r'Date First Available',item):
			dt_pattern = re.compile(r'([a-z]*) ([0-9]*), ([0-9]*)',re.I)
			dt_target = dt_pattern.search(tr.find("td").string)
			if dt_target != None:
				dt_format = datetime.datetime.strptime(str(dt_target.group()),'%B %d, %Y')
				date = dt_format.strftime('%Y-%m-%d')
			print("Get date successfully")
			#print(date)

	details.append(oneASIN)
	details.append(review)
	details.append(star)
	details.append(rank[0])
	details.append(category[0])
	details.append(rank[1])
	details.append(category[1])
	details.append(rank[2])
	details.append(category[2])
	details.append(date)

	return details


while True:
	wbk_rd = xlrd.open_workbook('ProductDetails.xls')
	asin_sheet_rd = wbk_rd.sheet_by_name('AllASIN')
	index_now = int(asin_sheet_rd.cell(0,1).value)
	index_end = int(asin_sheet_rd.cell(1,1).value)
	row_nml = int(asin_sheet_rd.cell(2,1).value)
	row_err = int(asin_sheet_rd.cell(3,1).value)
	asin = asin_sheet_rd.cell(index_now,0).value

	wbk_wt = copy(wbk_rd)

	asin_detail = get_detail_of_oneASIN(asin)
	if len(asin_detail)==1:
		sheet_err = wbk_wt.get_sheet('ErrorASIN')
		sheet_err.write(row_err,0,asin_detail[0])
		row_err = row_err+1
	else:
		for i in range(0,len(asin_detail)):
			sheet_nml = wbk_wt.get_sheet('ProductDetails')
			if isinstance(asin_detail[i],str):
				detail_tmp = asin_detail[i].decode('utf-8')
			else:
				detail_tmp = asin_detail[i]
			sheet_nml.write(row_nml,i,detail_tmp)
		row_nml = row_nml + 1
	asin_sheet_wt = wbk_wt.get_sheet('AllASIN')
	index_now = index_now + 1
	asin_sheet_wt.write(0,1,index_now)
	asin_sheet_wt.write(2,1,row_nml)
	asin_sheet_wt.write(3,1,row_err)
	
	wbk_wt.save('ProductDetails.xls')

	if index_now == index_end:
		break

