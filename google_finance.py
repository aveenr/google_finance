from bs4 import BeautifulSoup
import requests

# INIT JSE CODE AND LINKS
SYMBOLS = 'BIL'
GOOGLE_FINANCE_URL = 'https://www.google.com/finance'
GOOGLE_FINANCE_HISTORICAL_URL = 'https://www.google.com/finance/historical'
code_url = GOOGLE_FINANCE_URL + '?q=JSE%3A' + SYMBOLS

# OPEN JSE CODE PAGE IN GOOGLE FINANCE
request = requests.get(code_url)
content = request.content
soup = BeautifulSoup(content, 'html.parser')
parsed = soup.find_all('link', {'rel': 'canonical'})

# FIND CID CODE
for cid in parsed:
    # HARDCODED FOR CID ID
    cid_code = cid['href'][34:]

# INIT DATE PARAMS
start_month = 'Mar+'
start_day = '10%2C+'
start_year = '2016'
start_date = start_month + start_day + start_year
end_month = 'Mar+'
end_day = '22%2C+'
end_year = '2017'
end_date = end_month + end_day + end_year

# OUTPUT DOWNLOAD LINK
historical_url = (GOOGLE_FINANCE_HISTORICAL_URL + '?cid=' + cid_code + '&startdate=' + start_date + '&enddate=' + end_date + '&output=csv')

# OUPUT TO SCREEN
# request = requests.get(a)
# content = request.content
# soup = BeautifulSoup(content, 'html.parser')

# DOWNLOAD TO LOCAL DIRECTORY
with open(SYMBOLS + '.csv', 'wb') as handle:
    response = requests.get(historical_url, stream=True)
    if not response.ok:
        print('File could not be downloaded')
    for block in response.iter_content(1024):
        handle.write(block)
