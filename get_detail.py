import urllib2
import re
from bs4 import BeautifulSoup

import time
import datetime
import random

import xlwt
import xlrd
from xlutils.copy import copy

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent' : ua.random}

def get_detail_of_table_1(table):
	detail = []
	sonASIN = '0'
	review = 0
        star = 0.0
        rank = [0,0,0]
        category = ['0','0','0']
        date = '0000-00-00'

	all_tr = table.find_all("tr")
	if len(all_tr)==0:
		print("Error: tr not found, return errASIN")
        	return None

	for tr in all_tr:
		item = tr.find("th").string
		value = tr.find("td")
		
		if re.search(r'ASIN',item):
			as_pattern = re.compile(r'B([A-Z0-9]*)',re.I)
			as_target = as_pattern.search(value.string)
			if as_target != None:
				sonASIN = str(as_target.group())
			print("Get ASIN successfully")

		elif re.search(r'Customer Review',item):
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
			
		elif re.search(r'Date First Available',item):
			dt_pattern = re.compile(r'([a-z]*) ([0-9]*), ([0-9]*)',re.I)
			dt_target = dt_pattern.search(value.string)
			if dt_target != None:
				dt_format = datetime.datetime.strptime(str(dt_target.group()),'%B %d, %Y')
				date = dt_format.strftime('%Y-%m-%d')
			print("Get date successfully")
			
	detail.append(sonASIN)
	detail.append(review)
	detail.append(star)
	detail.append(date)
	detail.append(rank[0])
	detail.append(category[0])
	detail.append(rank[1])
	detail.append(category[1])
	detail.append(rank[2])
	detail.append(category[2])
	
	return detail



def get_detail_of_table_2(table):
	detail = []
	sonASIN = '0'
	review = 0
        star = 0.0
        rank = [0,0,0]
        category = ['0','0','0']
        date = '0000-00-00'

	all_li = table.find_all("li")
	if len(all_li) == 0:
		print("Error: li not found, return errASIN")
		return None

	for li in all_li:
		value = li
		item = li.b.extract()
		
		if re.search(r'ASIN',str(item)):
			as_pattern = re.compile(r'B([A-Z0-9]*)',re.I)
			as_target = as_pattern.search(value.string)
			if as_target != None:
				sonASIN = str(as_target.group())
			print("Get ASIN successfully")

		elif re.search(r'Customer Review',str(item)):
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
			
		elif re.search(r'Best Sellers Rank',str(item)):
			rk_pattern = re.compile(r'#([0-9,]*) in',re.I)
			rk_target = rk_pattern.search(str(value))
			if rk_target != None:
				rank[0] = int(rk_target.group(1).replace(',',''))
				category[0] = str(value.find("a").get_text())

			rk_k = 1
			all_li_son = value.find_all("li")
			for li_son in all_li_son:
				span = li_son.find_all("span")
				for sp_k in range(0,2):
					rank[rk_k]=int(str(span[0].get_text()).replace('#','').replace(',',''))
					category[rk_k]=str(span[1].get_text())
				rk_k = rk_k+1
				if rk_k == 3:
					break;
			print("Get rank successfully")
			
		elif re.search(r'Date First Available',str(item)):
			dt_pattern = re.compile(r'([a-z]*) ([0-9]*), ([0-9]*)',re.I)
			dt_target = dt_pattern.search(value.string)
			if dt_target != None:
				dt_format = datetime.datetime.strptime(str(dt_target.group()),'%B %d, %Y')
				date = dt_format.strftime('%Y-%m-%d')
			print("Get date successfully")
			
	detail.append(sonASIN)
	detail.append(review)
	detail.append(star)
	detail.append(date)
	detail.append(rank[0])
	detail.append(category[0])
	detail.append(rank[1])
	detail.append(category[1])
	detail.append(rank[2])
	detail.append(category[2])
	
	return detail



def get_detail_of_oneASIN(oneASIN):
	print("\nASIN:"+oneASIN)
	errASIN = []

	addr = "https://www.amazon.com/dp"+oneASIN
	req = urllib2.Request(addr,headers=headers)
	for try_num in range(0,10):	
		try:
			print(str(try_num)+"-th trying")
        		response = urllib2.urlopen(req,timeout=45)
        		raw_html = response.read()
			print("Get html page successfully")
			break
		except:
			if try_num == 9:
				print("The html page cannot be reached, quit it. Return errASIN.")
				errASIN.append(oneASIN)
				return errASIN
			print("Failed to get page, waiting 10s-15s and try again")
			time.sleep(random.randint(10,15))

	bsObj = BeautifulSoup(raw_html,'html.parser')
	table1 = bsObj.find("table",id="productDetails_detailBullets_sections1")
	all_table2 = bsObj.find_all("table",cellpadding=True,cellspacing=True)
	for tab in all_table2:
		if(re.search(r'Product details',str(tab)) != None):
			table2 = tab
		else:
			table2 = None
	if table1 != None:
		details = get_detail_of_table_1(table1)
	else:
		if len(all_table2)==0:
			print("Error: Table not found! Return errASIN")
                        errASIN.append(oneASIN)
                        return errASIN
		elif table2 != None:
			details = get_detail_of_table_2(table2)
		else:
			print("Error: Both tables not found! Return errASIN")
			errASIN.append(oneASIN)
			return errASIN

	if details == None:
		errASIN.append(oneASIN)
		return errASIN
	else:
		details.insert(0,oneASIN)
		return details

		
def get_details_of_allASIN():
	time.sleep(random.randint(0,5))
	while True:
		wbk_rd = xlrd.open_workbook('ProductDetails.xls')
		index_sheet_rd = wbk_rd.sheet_by_name('Index')
		id_index_now = int(index_sheet_rd.cell(1,0).value)
		id_index_end = int(index_sheet_rd.cell(2,0).value)
		asin_row_err = int(index_sheet_rd.cell(3,0).value)
		col = id_index_now+1
		id_now = str(index_sheet_rd.cell(0,col).value)
		asin_index_now = int(index_sheet_rd.cell(1,col).value)
		asin_index_end = int(index_sheet_rd.cell(2,col).value)
		asin_row_nml = int(index_sheet_rd.cell(3,col).value)

		info_sheet_rd = wbk_rd.sheet_by_name('AllASIN')
		asin_rd = info_sheet_rd.cell(asin_index_now+1,6*col-6).value
		price_rd = info_sheet_rd.cell(asin_index_now+1,6*col-5).value
		image_rd = info_sheet_rd.cell(asin_index_now+1,6*col-2).value
		title_rd = info_sheet_rd.cell(asin_index_now+1,6*col-1).value

		wbk_wt = copy(wbk_rd)

		asin_detail = get_detail_of_oneASIN(asin_rd)
		if len(asin_detail)==1:
			sheet_err = wbk_wt.get_sheet('ErrorASIN')
			sheet_err.write(asin_row_err,0,asin_detail[0])
			asin_row_err = asin_row_err+1
		else:
			asin_detail.insert(2,price_rd)
			asin_detail.insert(3,image_rd)
			asin_detail.insert(4,title_rd)
			for i in range(0,len(asin_detail)):
				sheet_nml = wbk_wt.get_sheet(id_now)
				if isinstance(asin_detail[i],str):
					detail_tmp = asin_detail[i].decode('utf-8')
				else:
					detail_tmp = asin_detail[i]
				sheet_nml.write(asin_row_nml,i,detail_tmp)
			asin_row_nml = asin_row_nml + 1

		index_sheet_wt = wbk_wt.get_sheet('Index')
		asin_index_now = asin_index_now + 1
		if asin_index_now == asin_index_end:
			id_index_now = id_index_now+1
		index_sheet_wt.write(1,0,id_index_now)
		index_sheet_wt.write(1,col,asin_index_now)
		index_sheet_wt.write(3,col,asin_row_nml)
		index_sheet_wt.write(3,0,asin_row_err)
	
		wbk_wt.save('ProductDetails.xls')

		if id_index_now == id_index_end:
			break


#asin_detail = get_detail_of_oneASIN("/B07BS7P7T6/")
#print(asin_detail)

get_details_of_allASIN()
