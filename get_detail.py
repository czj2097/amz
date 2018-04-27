import urllib2
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent' : ua.random}

#addr = 'https://www.amazon.com/dp/B07B6F5PJ7/'
#req = urllib2.Request(addr,headers=headers)
#response = urllib2.urlopen(req)
#raw_html = response.read()

with open('../amazon_origin.html','r') as f:
        raw_html = f.read()

bsObj = BeautifulSoup(raw_html,'html.parser')
all_tr = bsObj.find("table",id="productDetails_detailBullets_sections1").find_all("tr")
for tr in all_tr:
	item = tr.find("th").string
	value = tr.find("td")

	if re.search(r'Customer Reviews',item):
		review = '0'
		star = '0'
		all_a = value.find_all("a")
		for a in all_a:
			rw_pattern1 = re.compile(r'([0-9]*) customer reviews',re.I)
			rw_pattern2 = re.compile(r'([0-9]*\.[0-9]*) out of 5 stars',re.I)
			rw_target1 = rw_pattern1.search(str(a))
			rw_target2 = rw_pattern2.search(str(a))
			if rw_target1 != None:
				review = rw_target1.group(1)
			if rw_target2 != None:
				star = rw_target2.group(1)
		print(review)
		print(star)
	elif re.search(r'Best Sellers Rank',item):
		rank = ['0','0','0']
		category = ['0','0','0']
		rk_k = 0
		all_span = value.span.find_all("span")
		for span in all_span:
			rk_pattern1 = re.compile(r'#([0-9]*) in',re.I)
			rank[rk_k] = rk_pattern1.search(str(span)).group(1)
			category[rk_k] = str(span.get_text())
			rk_k = rk_k+1
		print(rank)
		print(category)

	elif re.search(r'Date First Available',item):
		date = ['0','0','0']
		dt_pattern = re.compile(r'([a-z]*) ([0-9]*), ([0-9]*)',re.I)
		dt_target = dt_pattern.search(tr.find("td").string)
		date[0] = str(dt_target.group(1))
		date[1] = str(dt_target.group(2))
		date[2] = str(dt_target.group(3))
		print(date)
