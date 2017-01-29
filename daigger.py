"""
@author Venita Boodhoo
Website: daigger
Status: Complete
Comments: For new equipment only
May return just a result on one page
"""
import urllib2
from bs4 import BeautifulSoup
from util import *
from Result import Result

MAIN_URL = "http://www.daigger.com/products-search?qs="
HOME_URL = "http://www.daigger.com"                    
DELIMITER = "+"

def extract_results(item,condition=None):
        results=[]
        if condition != "new":
                return results
        specific_url = create_url(MAIN_URL,item,DELIMITER)
        page = urllib2.urlopen(specific_url)
        soup = BeautifulSoup(page,"html.parser" )

        table = soup.find('div',id ="ListingProducts")

        try:
                  #Items are a list
                  rows=table.find_all('div',class_="boxshad productbox")
        except:
                  try:
                          #Returns one item on a specific pg
                          new_result = Result(soup.find('h1',itemprop='name'))
                          new_result.url = specific_url
                          new_result.image_src = HOME_URL+soup.find('div',class_='product-image').find('img').get('src')
                          items = soup.find_all('tr',class_='ejs-addtocart-section')
                          for item in items:
                                #Supplier #
                                supplier = item.find('span',class_='supplier-code')
                                if supplier != None:
                                        new_result.title = new_result.title + supplier.text
                                new_result.price = item.find('strong',class_='price').text
                                currency = item.find('span',itemprop='priceCurrency')
                                if currency == None and is_valid_price(new_result.price):
                                        results.append(new_result)
                                elif currency.text == "USD" and is_valid_price(new_result.price):
                                        results.append(new_result)
                                #Reset title
                                new_result.title = soup.find('h1',itemprop='name').text
                          
                          return results
                  except:
                          return []
        
        #For multiple items  
        for row in table.find_all('div',class_="boxshad productbox"):
                new_result = Result(row.find('a').get('title'))
                new_result.url = HOME_URL + row.find('a').get('href')
                print new_result.url
                new_result.image_src = HOME_URL + row.find('img').get('src')
                print new_result.image_src
                specific_page = urllib2.urlopen(new_result.url)
                new_soup = BeautifulSoup(specific_page,"html.parser")
                #Get all models of products from specific page
                items = new_soup.find_all('tr',class_='ejs-addtocart-section')
                for item in items:
                        #Supplier #
                        supplier = item.find('span',class_='supplier-code')
                        if supplier != None:
                                new_result.title = new_result.title + supplier.text
                        new_result.price = item.find('strong',class_='price').text
                        currency = item.find('span',itemprop='priceCurrency')
                        if currency == None and is_valid_price(new_result.price):
                                results.append(new_result)                         
                        elif currency.text == "USD" and is_valid_price(new_result.price):
                                results.append(new_result)
                        #Reset title
                        new_result.title = row.find('a').get('title')
                
        return results

def main():
    print extract_results("pump","new")

if __name__ == "__main__": main()
