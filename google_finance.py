from bs4 import BeautifulSoup
import requests

# INIT JSE CODE AND LINKS
code = 'BIL'
goog_finc = 'https://www.google.com/finance'
goog_finc_hist = 'https://www.google.com/finance/historical'
code_url = goog_finc+'?q=JSE%3A'+code

# OPEN JSE CODE PAGE IN GOOGLE FINANCE
request = requests.get(code_url)
content = request.content
soup = BeautifulSoup(content,'html.parser')
parsed = soup.find_all('link',{'rel':'canonical'})

# FIND CID CODE
for cid in parsed:
    # HARDCODED FOR CID ID
    cid_code = cid['href'][34:]
    print(cid_code)
    
# INIT DATE PARAMS
start_month = 'Mar+'
start_day = '10%2C+'
start_year = '2017'
start_date = start_month + start_day + start_year
end_month = 'Mar+'
end_day = '22%2C+'
end_year = '2017'
end_date = end_month + end_day + end_year

# OUTPUT DOWNLOAD LINK
a = (goog_finc_hist + '?cid=' + cid_code + '&startdate=' + start_date + '&enddate=' + end_date + '&output=csv')
print(a)
