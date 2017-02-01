from Result import Result
#import the 14 websites
import ebay
import marshallscientific
import equipnet
import google
import medwow
import used_line
import eurekaspot
import labcommerce
import newlifescientific
import labx
import biosurplus
import sci_bay
import dotmed
import sibgene

import util 
import math

USED_FUNCS=[equipnet.extract_results, \
labx.extract_results, \
ebay.extract_results, \
dotmed.extract_results, \
google.extract_results, \
biosurplus.extract_results, \
medwow.extract_results, \
labcommerce.extract_results, \
marshallscientific.extract_results, \
newlifescientific.extract_results, \
eurekaspot.extract_results, \
sci_bay.extract_results, \
sibgene.extract_results, \
used_line.extract_results ]

#split functions into groups to prevent timeouts
FUNC_DIC={'1': USED_FUNCS[:7], '2' : USED_FUNCS[7:], "all": USED_FUNCS, None: USED_FUNCS[:7]}

WEBSITE_NAMES={ebay.extract_results : "ebay" , equipnet.extract_results : "equipnet" , google.extract_results : "google" , used_line.extract_results : "used line", \
eurekaspot.extract_results : "eurekaspot", labcommerce.extract_results :"labcommerce", newlifescientific.extract_results :"newlifescientific", biosurplus.extract_results: "biosurplus" , sci_bay.extract_results : "sci_bay", \
dotmed.extract_results : "dotmed" , sibgene.extract_results: "sibgene" , labx.extract_results : "labx", medwow.extract_results: "medwow", marshallscientific.extract_results: \
"marshallscientific"}

MATCH_RATIO=.8

MAX_RESULTS=10

MIN_RESULTS=3


'''
searches the websites in func_group until MAX_RESULTS close results are found or all the websites are searched
returns search_successful (boolean), message (string), results (list of Results)
'''

def do_search(search_term, condition=None, func_group='1'):
    results=[]
    error_message=""
    functions=FUNC_DIC[func_group]
    for func in functions:
        try:
            print "scraping ",  WEBSITE_NAMES[func]
            website_results=func(search_term, condition)
            for website_result in website_results:
                if is_close_match(search_term, website_result.title):
                    results.append(website_result)
                    results.sort(key=lambda x: x.price, reverse=True)
                if len(results) >=MAX_RESULTS:
                    return True, error_message, results
        except Exception, e: 
            print "error scraping ",  WEBSITE_NAMES[func]
            print "Error was: ", e.message 
            error_message=error_message + "Error scraping %s.\n" %(WEBSITE_NAMES[func])
        if len(results) >= MAX_RESULTS:
            return True, error_message, results
    if len(results) < MIN_RESULTS:
        return False, error_message, results
    return True, error_message, results

'''
checks if the result contains at least MATCH_RATIO of the search words
'''
def is_close_match(search_term, result_term):
    search_words=search_term.split()
    match_number=0
    for word in search_words:
        if word.lower().strip() in result_term.lower():
            match_number+=1
    return match_number >= math.ceil(len(search_words)*MATCH_RATIO)


def main():
    print do_search("bio centrifuge")

if __name__ == "__main__": main()
