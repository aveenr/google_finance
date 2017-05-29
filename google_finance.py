from bs4 import BeautifulSoup
import requests
from time import localtime, strftime

# INIT JSE CODE AND LINKS
INPUT_SYMBOLS = ['agl','bil'] #input jse codes here
GOOGLE_FINANCE_URL = 'https://www.google.com/finance'
GOOGLE_FINANCE_HISTORICAL_URL = 'https://www.google.com/finance/historical'
EXCHANGE = '?q=JSE%3A'
YEARS = 20

# INIT DATE PARAMS
# Mar+1%2C+2000
back_year = ((int(strftime('%Y')) - YEARS))
start_date = (strftime('%b+' + '%d' + '%%2C+')) + str(back_year)
end_date = (strftime('%b+' + '%d' + '%%2C+' + '%Y'))

for SYMBOLS in INPUT_SYMBOLS:
    # OPEN JSE CODE PAGE IN GOOGLE FINANCE
    print('downloading ' + SYMBOLS.upper(), end='...', flush=True)
    SYMBOL_URL = GOOGLE_FINANCE_URL + EXCHANGE + SYMBOLS
    request = requests.get(SYMBOL_URL)
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')
    parsed = soup.find_all('link', {'rel': 'canonical'})

    # GET CID CODE (GOOGLE FINANCE CANONICAL CODE FOR A SECURITY)
    for cid in parsed:
        cid_code = cid['href'][34:] # HARDCODED FOR CID ID

    # GET GOOGLE FINANCE DOWNLOAD LINK
    historical_url = (GOOGLE_FINANCE_HISTORICAL_URL + '?cid=' + cid_code +
                      '&startdate=' + start_date + '&enddate=' + end_date +
                      '&output=csv')

    # DOWNLOAD TO LOCAL DIRECTORY
    with open(SYMBOLS.lower() + '.csv', 'wb') as handle:
        response = requests.get(historical_url, stream=True)
        if not response.ok:
            print('File could not be downloaded')
        for block in response.iter_content(1024):
            handle.write(block)
    print('done')
