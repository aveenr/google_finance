import requests
import logging
import os
import errno
from datetime import date
import datetime
import argparse

class GoogleFinanceDownload(object):
    """ Google Finance Downloader that downloads historical data for a list of stocks """
    def __init__(self, period, data_file_name, download_directory, exchange):
        self.url = 'https://www.google.com/finance/historical'
        self.period = period
        self.file = data_file_name
        self.download_directory = download_directory
        self.exchange = exchange
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
            os.makedirs(self.download_directory)
            os.chdir(self.download_directory)
            logging.info('Directory set to %s', self.download_directory)
        except OSError as exception:
            if exception.errno == errno.EEXIST:
                os.chdir(self.download_directory)
            else:
                raise

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
        historical_payload = {'q': self.exchange + ':' + stock, 'output': 'csv',
                             'startdate':self.query_string_date(self.period),
                              'enddate':self.query_string_date()}
        print(historical_payload)
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
    parser.add_argument('-e', '--exchange', help='Name of exchange (default = JSE', default='JSE')
    parser.add_argument('-p', '--path', help='Directory name for download', default='stocks')
    parser.add_argument('-t', '--time', help='Years to count back (default = 1 year)', type=int, default=1)
    args = parser.parse_args()

    # init class
    JSE_Download = GoogleFinanceDownload(period=args.time, data_file_name=args.filename, download_directory=args.path, exchange=args.exchange)

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
