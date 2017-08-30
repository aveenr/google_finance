import requests
from time import strftime
import logging
import os
import errno
import datetime
from datetime import date

url = 'https://www.google.com/finance/historical'

period = 1 #daily versus full download
data_file = 'stocks'
root_dir = './'
dl_dir = 'git'
dl_path = os.path.join(root_dir, dl_dir)
invalid = []

def get_stocks(stocks_file=data_file):
    try:
        with open(stocks_file + '.txt', 'r') as data_file:
            stocks = (data_file.read()).split()
            # read into list needs validation
    except IOError:
        print('ERROR: File Not found')
        exit(1)
    logging.info('Contents of data file %s : ',stocks)
    make_dir()  #directory created for downloads
    return stocks

def make_dir():
    try:
        os.makedirs(dl_path)
        os.chdir(dl_path) #make directory and change to it
        logging.info('Directory %s', dl_path)
    except OSError as exception:
        if exception.errno == errno.EEXIST:  # and os.path.isdir(file_path):
            os.chdir(dl_path) #if directory exists, then change to it
        else:
            raise  # something else happened

def logger_name():
    return (datetime.datetime.today().strftime('%Y%m%d_%H%M%S'))+'.log'

def query_string_date(years=0):
    Y = date.today().year
    M = date.today().month
    D = date.today().day
    return (date(Y - years, M, D).strftime('%b %d %Y'))

def download_historical_data(url, stock):
    logging.info('Current stock is %s',stock.upper())
    historical_payload = {'q':'jse:'+stock,'output':'csv','startdate':query_string_date(period),'enddate':query_string_date()}
    # historical_payload = {'q': 'jse:' + stock, 'output': 'csv', 'startdate': start_date(), 'enddate': end_date()}
    logging.info('Payload data %s', historical_payload)
    # don't need the following two line, just logging
    r = requests.get(url, params=historical_payload)
    logging.info('URL sent %s', r.url)
    if r.status_code == 400:
            invalid.append(stock)
            logging.info('Invalid stock %s', stock.upper())
    else:
        data_count = 0
        with open(stock.lower() + '.csv', 'wb') as file_handle:
            for block in r.iter_content(1024):
                data_count += len(block)
                file_handle.write(block)
            print(stock.upper() + ' is complete')
    # logging.info('Downloaded size %s', math.ceil(data_count/1024))

def main():
    logging.basicConfig(filename=logger_name(), level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
    for symbol in get_stocks(): #through list not textfile
        try:
            download_historical_data(url, symbol)
        except requests.exceptions.RequestException as e:
            logging.info('Error in connection %s ', e)
            break
    logging.info('%s', invalid)

if __name__ == '__main__':
    main()
