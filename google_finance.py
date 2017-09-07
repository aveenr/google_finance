import requests
# from time import strftime
import logging
import os
import errno
import datetime
from datetime import date
import argparse

class GoogleFinanceDownload(object):
    """ Google Finance Downloader that downloads historical data for a list of stocks """
    def __init__(self, period, data_file_name, dl_path):
        self.url = 'https://www.google.com/finance/historical'
        self.period = period
        self.file = data_file_name
        self.dl_path = dl_path
        self.invalid = []
        self.stocks = []

    def get_stocks(self):
        """" Get stocks data from text file """
        try:
            with open(self.file, 'r') as data_file:
                self.stocks = (data_file.read()).split()
        except IOError:
            print('ERROR: {0} File Not found'.format(self.file))
            exit(1)
        logging.info('Contents of data file %s : ',self.stocks)
        self.make_dir()  #directory created for downloads
        return self.stocks

    def class_dump(self):
        """Dump object to screen"""
        print(self.__dict__)

    def make_dir(self):
        """ Creates the destination directory """
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
        return (datetime.datetime.today().strftime('%Y%m%d_%H%M%S'))+'.log'

    def query_string_date(self, years=0):
        """" Create date string for url """
        Y = date.today().year
        M = date.today().month
        D = date.today().day
        return (date(Y - years, M, D).strftime('%b %d %Y'))

    def download_csv(self, stock):
        """" Downloads csv file from Google Finance """
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
    parser = argparse.ArgumentParser(description='Google Finance Downloader: Downloads historical data of list of stocks as csv files')
    parser.add_argument('-f', '--filename', help='Path to file containing stocks to download', default='stocks.txt')
    ## feature to add parser.add_argument('--exchange', '-e', help='Name of exchange (default=JSE', nargs='*', default='JSE')
    parser.add_argument('-p', '--path', help='Directory name for download', default='stocks')
    parser.add_argument('-t', '--time', help='Years to count back (default = 1 year)', type=int, default=1)
    args = parser.parse_args()

    # init class
    JSE_Download = GoogleFinanceDownload(period=args.time, data_file_name=args.filename, dl_path=args.path)

    # init logger
    logging.basicConfig(filename=JSE_Download.logger_name(),
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y/%m/%d %I:%M:%S %p')
    # main
    for stock in JSE_Download.get_stocks():
        try:
            JSE_Download.download_csv(stock)
        except requests.exceptions.RequestException as e:
            logging.info('Error in connection %s ', e)
            break
    logging.info('%s', JSE_Download.invalid)

if __name__ == '__main__':
    main()
