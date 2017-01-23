"""
@author Venita Boodhoo
Website: EurekaSpot
Status: Description debug
Comment: Search only single words, NOT multiple words because
         their web search engine includes the "20" between
         words when it should be recognized as a space
         
         e.g. bio%20pump should search bio pump but their
         code makes it search "bio20pump" which unfortunately
         I cannot change :(

         Same thing with "+"

Assumes all items are used on this website
"""

import urllib2
from bs4 import BeautifulSoup
from util import *
from Result import Result

main_url = "http://www.eurekaspot.com"
search_url = "http://www.eurekaspot.com/estore/searchtmp2.cfm?quiksrch_keywords="
DELIMITER ="%20"

def extract_results(item,condition=None):
        results=[]
        if condition != "new":
                search_term=get_good_search_term(item)
                page = urllib2.urlopen(create_url(search_url,search_term,DELIMITER))
                soup = BeautifulSoup(page,"html.parser" )
                table = soup.find_all('td',class_='productname')
                for row in table:
                        new_result = Result(row.find('a').text)
                        specific_url = main_url+row.find('a').get('href')
                        new_result.url = re.sub('%2E','.',specific_url)
                        new_result.image_src = main_url+\
                                               soup.find_all('td',class_='image')[0].find('img').get('src')
                        specific_page = urllib2.urlopen(new_result.url)
                        new_soup = BeautifulSoup(specific_page,"html.parser")
                        try:
                            new_result.price = get_price(new_soup.find('span',class_='sellprice').text)
                        except:
                            continue
                        #Code to add only functional items
                        description_url = main_url+re.sub(' ','%20',new_soup.find('p',id='name').find('a').get('href'))
                        description_page = urllib2.urlopen(description_url)
                        description_soup = BeautifulSoup(description_page,"html.parser")

                        functional_tag = description_soup.find(text='Functional:')
                        working = functional_tag.find_next('td').text
                        if "yes" in working or "Yes" in working and is_valid_price(new_result.price):
                                description_tag = description_soup.find(text='Seller comments:') 
                                #new_result.description = description_tag.find_next('td').text.decode('utf-8', 'ignore').encode('utf-8', 'ignore')
                                results.append(new_result)                                                
                        
        return results

'''
Added by Abigail
Finds a term that looks like a model number (contains a digit) and returns that term
If no terms containing digits exist, returns first word 
'''
def get_good_search_term(search_terms):
    terms=search_terms.split()
    for term in search_terms.split():
        if any(char.isdigit() for char in term):
            return term
    return "" if len(terms)==0 else terms[0]

def main():
    print extract_results("pump HX7400")

if __name__ == "__main__": main()
