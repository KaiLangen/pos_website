# -*- coding: utf-8 -*-

import scrapy
import pos_scrapy.items as items
from pos_scrapy.settings import *
from glob import glob
from csv import DictReader
from dashboard.models import CustomerOrder, Transaction

DO_NOT_PROCESS_TEST = True

START_URL = 'https://i5.gomjfreeway.com/sherimjfreeway/'


class GomjfreewaySpider(scrapy.Spider):
    name = "gomjfreeway"
    allowed_domains = None
    start_urls = None
    handle_httpstatus_list = [404, 403, 200, 405]

    def __init__(self, **kwargs):
        self.test = kwargs.get('test', None)
        self.test_url = 'test_url' in kwargs

        if 'test_url' in kwargs:
            self.test_url = kwargs['test_url']

        super(GomjfreewaySpider, self).__init__()

    def start_requests(self):
        if self.test_url:
            yield scrapy.Request(self.test_url, callback=self.parse)

        else:
            yield scrapy.Request(START_URL, callback=self.parse)

    def parse(self, response):
        if PROCESS_CSV:
            for item in self.process_csv():
                yield item

        else:
            return

    def process_csv(self):
        file_list = glob(CSV_PATH + '*_patients.csv')
        for file_path in file_list:
            with open(file_path) as csv_file:
                reader = DictReader(csv_file)
                for row in reader:
                    item = items.CustomerOrder()
                    item['table_type'] = 'customer_order'
                    item['source_type'] = 'gomjfreeway'
                    item['order_id'] = row['Order ID']

                    if not self.exists_order(item['order_id']):
                        try:
                            item['name'] = row['Patient']
                            item['source_id'] = row['Patient #']
                            item['member'] = row['Member?']
                            item['caregiver'] = row['Caregiver']
                            item['date'] = row['Purchase Date']
                            item['order_total'] = row['Order Total']
                            yield item
                        except KeyError:
                            self.logger.error('Invalid file format: {}'.format(file_path))

                    else:
                        self.logger.info('Item already exists, skipping')

        file_list = glob(CSV_PATH + '*_transactions.csv')
        for file_path in file_list:
            with open(file_path) as csv_file:
                reader = DictReader(csv_file)
                for row in reader:
                    item = items.Transaction()
                    item['table_type'] = 'transaction'
                    item['source_type'] = 'gomjfreeway'
                    item['order_id'] = row['Order ID']
                    item['description'] = row['Description']

                    if not self.exists_transaction(item['order_id'], item['description']):
                        try:
                            item['date'] = row['Date']
                            item['qty_dispensed'] = row['Qty Dispensed']
                            item['qty_sold'] = row['Qty Sold']
                            item['price'] = row['Price']
                            item['subtotal'] = row['Subtotal']
                            item['discount'] = row['Discount']
                            item['tax'] = row['Tax']
                            item['name'] = row['Customer']
                            item['cashier'] = row['Cashier']
                            yield item
                        except KeyError:
                            self.logger.error('Invalid file format: {}'.format(file_path))

                    else:
                        self.logger.info('Item already exists, skipping')

    def exists_order(self, order_id):
        try:
            CustomerOrder.objects.get(order_id=order_id, customer__source_type='gomjfreeway')
            return True
        except CustomerOrder.DoesNotExist:
            return False

    def exists_transaction(self, order_id, description):
        try:
            Transaction.objects.get(order__order_id=order_id, description=description,
                                    order__customer__source_type='gomjfreeway')
            return True
        except Transaction.DoesNotExist:
            return False
