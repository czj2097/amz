import random
import time
import urllib2
import re
from bs4 import BeautifulSoup

import xlwt
import xlrd
from xlutils.copy import copy

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from fake_useragent import UserAgent
ua = UserAgent()

def try_request(addr):
	headers = {'User-Agent' : ua.random}
	req = urllib2.Request(addr,headers=headers)

	print("Trying to connect the html......")
	for try_num in range(0,10):	
		try:
			response = urllib2.urlopen(req,timeout=45)
			raw_html = response.read()
			print("Get html page successfully")
			break
		except:
			if try_num == 9:
				print("The html page cannot be reached, quit it. Return errCategory.")
				return None
			print("Failed to get html, waiting 10s-15s and try again")
			time.sleep(random.randint(10,15))

	return raw_html



def get_info_of_50item(obj):
	ASINs = []
        Prices = []
        Reviews = []
        Stars = []
        Images = []
        Titles = []
        info = []
        error = False
	next_page = None

	#Get info in current page
	all_li = obj.find_all("li",class_="zg-item-immersion")
	if len(all_li)==0:
		print("li not found, different page appear. Return errCategory.")
		error = True
		return next_page,info,error


	for li in all_li:
		if re.search(r'/B([0-9A-Z]*)/',str(li)) != None:
			asin = re.search(r'/B([0-9A-Z]*)/',str(li)).group()
			
			price = 0.0
			target_prc = re.search(r'\$([0-9,]*)\.([0-9]*)',str(li))
			if target_prc != None:
				price = float(str(target_prc.group()).replace('$','').replace(',',''))
			
			star = 10.0
			review = 0
			all_a = li.find_all("a")
			for a in all_a:
				#print(a.get("href"))	
				rv_tar = re.search(r'review',str(a.get("href")),re.I)
				if rv_tar != None:
					star_tar = re.search(r'([0-9\.]*) out of 5 stars',str(a.get_text()),re.I)
					if star_tar != None:
						star = float(star_tar.group(1))
					else:
						review_tar = re.search(r'([0-9,])',str(a.get_text()))
						if review_tar != None:
							review = int(review_tar.group(1).replace(',',''))

			img = li.find("img")
			title = str(img.get("alt"))
			image = str(img.get("src"))

			#if price > 5 and price < 40 and review < 80 and star > 3.6:
			if True:
				ASINs.append(asin)
				Prices.append(price)
				Stars.append(star)
				Reviews.append(review)
				Images.append(image)
				Titles.append(title)
	
	info.append(ASINs)
	info.append(Prices)
	info.append(Stars)
	info.append(Reviews)
	info.append(Images)
	info.append(Titles)
	
	#Get addr of next page
	all_a = obj.find_all("a")
	for i in all_a:
        	if i.find(text = "Next page") != None:
 		        target_a = i
               		next_page = str(target_a.get('href'))
               		#print("next_page addr="+next_page)
	
	return next_page,info,error
	

def get_info_of_20item(obj,isFirst):
	ASINs = []
        Prices = []
        Reviews = []
        Stars = []
        Images = []
        Titles = []
        info = []
        error = False
	next_page = []

	#Get info in current page
	all_div = obj.find_all("div",class_="zg_itemImmersion")
	if len(all_div)==0:
		print("div not found, different page appear. Return errCategory.")
		error = True
		return next_page,info,error


	for div in all_div:
		if re.search(r'/B([0-9A-Z]*)/',str(div)) != None:
			asin = re.search(r'/B([0-9A-Z]*)/',str(div)).group()
			
			price = 0.0
			target_prc = re.search(r'\$([0-9,]*)\.([0-9]*)',str(div))
			if target_prc != None:
				price = float(str(target_prc.group()).replace('$','').replace(',',''))
			
			star = 10.0
			review = 0
			all_a = div.find_all("a")
			for a in all_a:
				#print(a.get("href"))	
				rv_tar = re.search(r'review',str(a.get("href")),re.I)
				if rv_tar != None:
					star_tar = re.search(r'([0-9\.]*) out of 5 stars',str(a.get_text()),re.I)
					if star_tar != None:
						star = float(star_tar.group(1))
					else:
						review_tar = re.search(r'([0-9,])',str(a.get_text()))
						if review_tar != None:
							review = int(review_tar.group(1).replace(',',''))

			img = div.find("img")
			title = str(img.get("alt"))
			image = str(img.get("src"))

			#if price > 5 and price < 40 and review < 80 and star > 3.6:
			if True:
				ASINs.append(asin)
				Prices.append(price)
				Stars.append(star)
				Reviews.append(review)
				Images.append(image)
				Titles.append(title)
	
	info.append(ASINs)
	info.append(Prices)
	info.append(Stars)
	info.append(Reviews)
	info.append(Images)
	info.append(Titles)
	
	#Get addr of next pages
	if isFirst == True:
		all_li = obj.find_all("li",class_="zg_page ")
		for li in all_li:
			target_a = li.find("a")
        		if target_a != None:
               			page = str(target_a.get('href'))
				next_page.append(page)
        	       		#print("next_page addr="+next_page)
	
	return next_page,info,error


def get_info_of_one_category(category_id):
	print("\ncategoryID:"+(category_id))

	info = [[],[],[],[],[],[]]
	next_info = [[],[],[],[],[],[]]
	errCategory = []
	
	#addr = 'https://www.amazon.com/gp/new-releases/hi/'+category_id
	addr = 'https://www.amazon.com/gp/bestsellers/hi/'+category_id
	#addr = 'https://www.amazon.com/gp/movers-and-shakers/'+category_id

	html = try_request(addr)
	if html == None:
		errCategory.append(category_id)
		return errCategory

	bsObj = BeautifulSoup(html,'html.parser')
	obj_50 = bsObj.find("div",id="zg-center-div")
	obj_20 = bsObj.find("div",id="zg_centerListWrapper")
	if obj_50 != None and obj_20 != None:
		print("Both page of 20 & 50 items found. Return errCategorry")
		errCategory = category_id
                return errCategory
	elif obj_50 != None and obj_20 == None:
		next_addr,info,error = get_info_of_50item(obj_50)
		if error == True:
			errCategory.append(category_id)
			return errCategory
		else:
			if next_addr != None:
				time.sleep(random.randint(0,5))
				next_html = try_request(next_addr)
				if next_html == None:
					print("Current page cannot be reached, ignore.")
				else:
					next_bsObj = BeautifulSoup(next_html,'html.parser')
					next_obj_50 = next_bsObj.find("div",id="zg-center-div")
					next_addr,next_info,error = get_info_of_50item(next_obj_50)
					if error == True:
						print("Two pages are of different type. Ignore current page.")
					else:
						for i in range(0,6):
							for j in range(0,len(next_info[0])):
								info[i].append(nex_info[i][j])
	elif obj_50 == None and obj_20 != None:
		next_addr,info,error = get_info_of_20item(obj_20,True)
		if error == True:
			errCategory.append(category_id)
                        return errCategory
		else:
			for addr in next_addr:
				time.sleep(random.randint(0,5))
				next_html = try_request(addr)
				if next_html == None:
					print("Current page cannot be reached, ignore.")
				else:
					next_bsObj = BeautifulSoup(next_html,'html.parser')
					next_obj_20 = next_bsObj.find("div",id="zg_centerListWrapper")
					next_addr,next_info,error = get_info_of_20item(next_obj_20,False)
					if error == True:
						print("Two pages are of different typr. Ignore current page")
					else:
						for i in range(0,6):
							for j in range(0,len(next_info[0])):
								info[i].append(next_info[i][j])		
	else:
		print("Both page of 20 & 50 item not found. Return errCategory")
		errCategory.append(category_id)
		return errCategory
	
	if(len(info[0])==0):
		return None
	else:	
		return info


def get_info_of_all_category():
	pd_title = ["Price","Review"]
	
	while True:
		time.sleep(random.randint(0,5))

		id_wbk_rd = xlrd.open_workbook('CategoryID.xls')
		id_sheet_rd = id_wbk_rd.sheet_by_name('CategoryID')
		index_now = int(id_sheet_rd.cell(0,1).value)
        	index_end = int(id_sheet_rd.cell(1,1).value)
        	row_nml = int(id_sheet_rd.cell(2,1).value)
        	row_err = int(id_sheet_rd.cell(3,1).value)
        	category_id_rd = str(int(id_sheet_rd.cell(index_now,0).value))
		id_wbk_wt = copy(id_wbk_rd)

		info = get_info_of_one_category(category_id_rd)
		if info == None:
			index_now = index_now + 1
			id_sheet_nml = id_wbk_wt.get_sheet('CategoryID')
                	id_sheet_nml.write(0,1,index_now)
                	id_wbk_wt.save('CategoryID.xls')
			if index_now == index_end:
				break
			else:
				continue
		elif len(info) == 1:
			id_sheet_err = id_wbk_wt.get_sheet('ErrorCategory')
                        id_sheet_err.write(row_err,0,info[0])
                        row_err = row_err+1
		else:
			ASINs = info[0]
                        Prices = info[1]
			Stars = info[2]
			Reviews = info[3]
                        Images = info[4]
                        Titles = info[5]

			new_sheet = id_wbk_wt.add_sheet(category_id_rd)
			new_sheet.write(0,0,pd_title[0])
			new_sheet.write(0,1,pd_title[1])
			for i in range(0,len(ASINs)):
				new_sheet.write(i+1,0,Prices[i])
				new_sheet.write(i+1,1,Reviews[i])

			row_nml = row_nml + 1

                id_sheet_nml = id_wbk_wt.get_sheet('CategoryID')
                index_now = index_now + 1
                id_sheet_nml.write(0,1,index_now)
                id_sheet_nml.write(2,1,row_nml)
                id_sheet_nml.write(3,1,row_err)
                id_wbk_wt.save('CategoryID.xls')
		
                if index_now == index_end:
                        break



#info = get_info_of_one_category('511228')
#print(info)
#print(len(info[0]))
get_info_of_all_category()
