
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 18:06:56 2017

@author: thotran
"""
import util
from Result import Result
import urllib2
from bs4 import BeautifulSoup

MAIN_URL="http://www.marshallscientific.com/searchresults.asp?Search="
DELIMITER='+'

#Marshall Scientific sells used equipment only. 
def extract_results(search_word, condition=None):
    if condition=="new":
        return []
    url=util.create_url(MAIN_URL,search_word,DELIMITER)
    page =urllib2.urlopen(url)
    soup=BeautifulSoup(page,"html.parser")
    product_grid=soup.find('div', class_='v-product-grid')
    try:
        total_equips=product_grid.find_all('div',class_='v-product')
    except:
        return []
    equips=[]
    for equip in total_equips:
        title=equip.find('a', class_='v-product__title productnamecolor colors_productname').find(text=True).strip()
        equipment=Result(title)
        equipment.url=equip.find('a',class_='v-product__img').get('href')
        equipment.image_src='http:'+equip.find('img').get('src')
        price_text=equip.find('div', class_='product_productprice').find_all(text=True)
        equipment.price=util.get_price(''.join(price_text))
        if util.is_valid_price(equipment.price):
            equips.append(equipment)
    return equips

def main():
    print exact_results('centrifuge')

if __name__=='__main__': main()
    
    
    
    






    
    
    
    
    
    
    

