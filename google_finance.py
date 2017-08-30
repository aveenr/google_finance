import requests
from time import strftime
import logging
import os
import errno
import datetime
from datetime import date

class myClass(object):
    def __init__(self, period=5, data_file_name='stocks.txt', dl_path='Github'):
        self.url = 'https://www.google.com/finance/historical'
        self.period = period
        self.file = data_file_name
        self.dl_path = dl_path

        # root_dir = './'
        # dl_dir = 'git'
        # self.dl_path = os.path.join(root_dir, dl_dir)

        self.invalid = []
        self.stocks = []

    def get_stocks(self):
        try:
            with open(self.file, 'r') as data_file:
                self.stocks = (data_file.read()).split()
        except IOError:
            print('ERROR: File Not found')
            exit(1)
        logging.info('Contents of data file %s : ',self.stocks)
        self.make_dir()  #directory created for downloads
        return self.stocks

    def class_dump(self):
        """Dump object to screen"""
        print(self.__dict__)

    def make_dir(self):
        try:
            os.makedirs(self.dl_path)
            os.chdir(self.dl_path) #make directory and change to it
            logging.info('Directory set to %s', self.dl_path)
        except OSError as exception:
            if exception.errno == errno.EEXIST:  # and os.path.isdir(file_path):
                os.chdir(self.dl_path) #if directory exists, then change to it
            else:
                raise  # something else happened

    def logger_name(self):
        return (datetime.datetime.today().strftime('z%Y%m%d_%H%M%S'))+'.log'

    def query_string_date(self, years=0):
        Y = date.today().year
        M = date.today().month
        D = date.today().day
        return (date(Y - years, M, D).strftime('%b %d %Y'))

    def download_historical_data(self, stock):
        logging.info('Current stock is %s',stock.upper())
        historical_payload = {'q':'jse:'+stock,'output':'csv',
                             'startdate':self.query_string_date(self.period),
                              'enddate':self.query_string_date()}
        logging.info('Payload data %s', historical_payload)
        r = requests.get(self.url, params=historical_payload)
        logging.info('URL sent %s', r.url)

        if r.status_code == 400:
                self.invalid.append(stock)
                logging.info('Invalid stock %s', stock.upper())
        else:
            data_count = 0
            with open(stock.lower() + '.csv', 'wb') as file_handle:
                for block in r.iter_content(1024):
                    data_count += len(block)
                    file_handle.write(block)
                print(stock.upper() + ' is complete')

def main():
    JSE_Download = myClass(dl_path='myJse', period=1)
    logging.basicConfig(filename=JSE_Download.logger_name(),
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y/%m/%d %I:%M:%S %p')

    for stock in JSE_Download.get_stocks():
        try:
            JSE_Download.download_historical_data(stock)
        except requests.exceptions.RequestException as e:
            logging.info('Error in connection %s ', e)
            break
        logging.info('%s', JSE_Download.invalid)
    # JSE_Download.class_dump()

if __name__ == '__main__':
    main()
