from bs4 import BeautifulSoup
import requests
from time import localtime, strftime

# INIT JSE CODE AND LINKS
SYMBOLS = 'bil'
BASE_SYMBOLS = ['oml','npn','agl']
GOOGLE_FINANCE_URL = 'https://www.google.com/finance'
GOOGLE_FINANCE_HISTORICAL_URL = 'https://www.google.com/finance/historical'
# code_url = GOOGLE_FINANCE_URL + '?q=JSE%3A' + SYMBOLS
YEARS = 20

for SYMBOLS in BASE_SYMBOLS:
    # OPEN JSE CODE PAGE IN GOOGLE FINANCE
    code_url = GOOGLE_FINANCE_URL + '?q=JSE%3A' + SYMBOLS
    request = requests.get(code_url)
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')
    parsed = soup.find_all('link', {'rel': 'canonical'})
    
    # FIND CID CODE
    for cid in parsed:
        # HARDCODED FOR CID ID
        cid_code = cid['href'][34:]
    
    # INIT DATE PARAMS
    # Mar+1%2C+2000
    back_year = ((int(strftime('%Y')) - YEARS))
    start_date = (strftime('%b+' + '%d' + '%%2C+')) + str(back_year)
    end_date = (strftime('%b+' + '%d' + '%%2C+' + '%Y'))
    
    # OUTPUT DOWNLOAD LINK
    historical_url = (GOOGLE_FINANCE_HISTORICAL_URL + '?cid=' + cid_code + '&startdate=' + start_date + '&enddate=' + end_date + '&output=csv')
    
    # OUPUT TO SCREEN
    # request = requests.get(a)
    # content = request.content
    # soup = BeautifulSoup(content, 'html.parser')
    
    # DOWNLOAD TO LOCAL DIRECTORY
    with open(SYMBOLS.lower() + '.csv', 'wb') as handle:
        response = requests.get(historical_url, stream=True)
        if not response.ok:
            print('File could not be downloaded')
        for block in response.iter_content(1024):
            handle.write(block)
