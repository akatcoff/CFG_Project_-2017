'''
Created by Abigail Katcoff
TODO: image src's are weird

'''

import util
import urllib2
from bs4 import BeautifulSoup
from Result import Result

MAIN_URL='https://www.google.com/search?output=search&tbm=shop&q='
DELIMITER= '+'

def extract_results(search_term, condition=None):
	url=util.create_url(MAIN_URL, search_term, DELIMITER)
	url = url + '&tbs=vw:l,mr:1,new:1' if condition=='new' else url
	headers={
	'Connection': 'keep-alive',
	'Accept': 'text/html',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
	req =urllib2.Request(url, headers=headers)
	page=urllib2.urlopen(req)
	soup = BeautifulSoup(page)
	table=soup.find('div', id='search')
	#table=soup.find('div', class_='sh-pr__product-results')
	rows=table.findAll('div', class_='psli')

	results=[]
	for row in rows:
		#ensure that if we're looking for used results to include used results only
		print row.find('span', class_='price')
		if condition!='new' and ('used' not in str(row.find('span', class_='price'))) :
			continue
		new_result=Result(row.find('a', class_='pstl').find(text=True))
		new_result.url='https://www.google.com'+row.find('a', class_='pstl').get('href')
		new_result.price=util.get_price(row.find('span', class_='price').b.find(text=True))
		new_result.image_src=row.find('img').get('src')
		if util.is_valid_price(new_result.price):
			results.append(new_result)
	return results


def main():
    print extract_results("Beckman Coulter Biomek Workstation")

if __name__ == "__main__": main()