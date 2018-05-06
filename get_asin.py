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
headers = {'User-Agent' : ua.random}

def get_info_of_one_category(category_id):
	print("\ncategoryID:"+(category_id))

	ASINs = []
	Prices = []
	Reviews = []
	Stars = []
	Images = []
	Titles = []
	info = []
	errCategory = []
	
	addr = 'https://www.amazon.com/gp/new-releases/hi/'+category_id
	#addr = 'https://www.amazon.com/gp/bestsellers/hi/'+category_id
	#addr = 'https://www.amazon.com/gp/movers-and-shakers/'+category_id

	k=0
	while True:
		req = urllib2.Request(addr,headers=headers)

		#Get page of 50 items, ignore page of 20 items
		for req_num in range(0,10):
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
						errCategory.append(category_id)
						return errCategory
					print("Failed to get html, waiting 10s-15s and try again")
					time.sleep(random.randint(10,15))

			bsObj = BeautifulSoup(raw_html,'html.parser')
			targetObj = bsObj.find("div",id="zg-center-div")
			if targetObj==None:
				print("Get page of 20 items, request again after 5s-10s")
				time.sleep(random.randint(5,10))
			else:
				print("Get page of 50 items at "+str(req_num)+"-th request")
				break
		if req_num == 9 and targetObj == None:
			print("Error: page of 50 items not exist. Each page has 20 items.")
			errCategory.append(category_id)
			return errCategory

		#Get product info in current page
		all_li = targetObj.find_all("li",class_="zg-item-immersion")
		if len(all_li)==0:
			print("li not found, different page appear. Return errCategory.")
			errCategory.append(category_id)
			return errCategory

		for li in all_li:
			if re.search(r'/B([0-9A-Z]*)/',str(li)) != None:
				asin = re.search(r'/B([0-9A-Z]*)/',str(li)).group()
				
				price = 0.0
				target_prc = re.search(r'\$([0-9,\.]*)',str(li))
				if target_prc != None:
					price = float(str(target_prc.group(1)).replace(',',''))
				
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

				#print("ASIN:"+str(asin))
				#print("target_price",target_prc)
				#print(price,review,star)
				#print('\n')

				if price > 5 and price < 40 and review < 80 and star > 3.6:
					#print("\n")
					ASINs.append(asin)
					Prices.append(price)
					Stars.append(star)
					Reviews.append(review)
					Images.append(image)
					Titles.append(title)
				
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

	if len(ASINs)==0:
		return None
	else:
		info.append(ASINs)
		info.append(Prices)
		info.append(Stars)
		info.append(Reviews)
		info.append(Images)
		info.append(Titles)
		return info


def get_info_of_all_category():
	pd_title = ["fatherASIN","sonASIN","Price","Image","Title","Review","Stars","Date","Rank1","RankDetail1","Rank2","RankDetail2","Rank3","RankDetail3"]
	
	while True:
		id_wbk_rd = xlrd.open_workbook('CategoryID.xls')
		id_sheet_rd = id_wbk_rd.sheet_by_name('CategoryID')
		index_now = int(id_sheet_rd.cell(0,1).value)
        	index_end = int(id_sheet_rd.cell(1,1).value)
        	row_nml = int(id_sheet_rd.cell(2,1).value)
        	row_err = int(id_sheet_rd.cell(3,1).value)
        	category_id_rd = str(int(id_sheet_rd.cell(index_now,0).value))
		id_wbk_wt = copy(id_wbk_rd)

		dt_wbk_rd = xlrd.open_workbook("ProductDetails.xls")
		dt_wbk_wt = copy(dt_wbk_rd)
		sheet_0 = dt_wbk_wt.get_sheet('Index')

		info = get_info_of_one_category(category_id_rd)
		if info == None:
			index_now = index_now + 1
			id_sheet_nml = id_wbk_wt.get_sheet('CategoryID')
                	id_sheet_nml.write(0,1,index_now)
                	id_wbk_wt.save('CategoryID.xls')
                	dt_wbk_wt.save('ProductDetails.xls')
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

			sheet_0.write(0,row_nml+1,category_id_rd)
			sheet_0.write(1,row_nml+1,0)
			sheet_0.write(2,row_nml+1,len(ASINs))
			sheet_0.write(3,row_nml+1,1)
			sheet_0.write(4,row_nml+1,0)

			sheet_2 = dt_wbk_wt.get_sheet('AllASIN')
			new_sheet = dt_wbk_wt.add_sheet(category_id_rd)

			sheet_2.write(0,6*row_nml,category_id_rd)
			for i in range(0,len(ASINs)):
				sheet_2.write(i+1,6*row_nml,ASINs[i])
				sheet_2.write(i+1,6*row_nml+1,Prices[i])
				sheet_2.write(i+1,6*row_nml+2,Stars[i])
				sheet_2.write(i+1,6*row_nml+3,Reviews[i])
				sheet_2.write(i+1,6*row_nml+4,Images[i].decode('utf-8'))
				sheet_2.write(i+1,6*row_nml+5,Titles[i].decode('utf-8'))

			for j in range(0,len(pd_title)):
				new_sheet.write(0,j,pd_title[j])

			row_nml = row_nml + 1

                id_sheet_nml = id_wbk_wt.get_sheet('CategoryID')
                index_now = index_now + 1
                id_sheet_nml.write(0,1,index_now)
                id_sheet_nml.write(2,1,row_nml)
                id_sheet_nml.write(3,1,row_err)
                id_wbk_wt.save('CategoryID.xls')
		
		sheet_0.write(0,0,'id_index')
		sheet_0.write(1,0,0)
		sheet_0.write(2,0,row_nml)
		sheet_0.write(3,0,0)		
		dt_wbk_wt.save('ProductDetails.xls')

                if index_now == index_end:
                        break



#info = get_info_of_one_category('511228')
#print(info)
#print(len(info[0]))
get_info_of_all_category()
