from bs4 import BeautifulSoup
import requests

import urllib

# INPUT JSE CODE
x_code = ['NPN','OML','SHP']
goog_finc = 'https://www.google.com/finance'
goog_finc_hist = 'https://www.google.com/finance/historical'

code=[]

for code in x_code:
    code_url = goog_finc+'?q=JSE%3A'+code

    # OPEN JSE CODE PAGE IN GOOGLE FINANCE
    request = requests.get(code_url)
    content = request.content
    soup = BeautifulSoup(content,'html.parser')
    parsed = soup.find_all('link',{'rel':'canonical'})

    # FIND CID CODE
    for cid in parsed:
        # CID LINK HREF LINK, FORMAT TO KEEP THE CODE
        cid_code = cid['href'][34:]
        print(cid_code)
        # yolo = x['href'][34:]

    # GET HISTORY PAGE
    # code_history_url = ('https://www.google.com/finance/historical?cid=' + cid +
    #                         '&startdate=' + 'start_date=' + '&enddate=' + end_date)

    start_month = 'Mar+'
    start_day = '1%2C+'
    start_year = '2017'
    start_date = start_month + start_day + start_year
    print(start_date)

    end_month = 'Mar+'
    end_day = '23%2C+'
    end_year = '2017'
    end_date = end_month + end_day + end_year
    print(end_date)


    # a = (goog_finc_hist + '?cid=' + cid_code + '&startdate=' + start_date + '&enddate=' + end_date)
    a = (goog_finc_hist + '?cid=' + cid_code + '&startdate=' + start_date + '&enddate=' + end_date + '&output=csv')

    request = requests.get(a)
    content = request.content
    soup = BeautifulSoup(content,'html.parser')

    print(soup)

    with open(code+'.csv', 'wb') as handle:
        response = requests.get(a, stream=True)
        if not response.ok:
            print('File could not be downloaded')
        for block in response.iter_content(1024):
            handle.write(block)

# http://www.google.com/finance/historical?cid=187562520823645&startdate=Mar23%2C2010&enddate=Mar22%2C2017
# http://www.google.com/finance/historical?cid=187562520823645&startdate=Mar23%2C2010&enddate=Mar22%2C2017&output=csv

# DOWNLOAD


# code_history_url = ('https://www.google.com/finance/historical?cid=' + cid +
#                     '&startdate=' + 'start_date=' + '&enddate=' + end_date)
