# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from dashboard.models import Customer, CustomerOrder, Transaction

logger = logging.getLogger('pipes')


class PosScrapyPipeline(object):
    def process_item(self, item, spider):
        if item['table_type'] == 'customer_order':
            try:
                cust = Customer.objects.get(source_id=item['source_id'], source_type=item['source_type'])
            except Customer.DoesNotExist:
                cust = Customer()
                cust.source_type = item['source_type']
                cust.source_id = item['source_id']
                cust.name = item['name']
                cust.save()
                logger.info(u'Added {}'.format(str(cust)))

            cust_ord = CustomerOrder()
            cust_ord.customer = cust
            cust_ord.order_id = item['order_id']
            if item['member'].lower().strip() == 'yes':
                cust_ord.member = True
            elif item['member'].lower().strip() == 'no':
                cust_ord.member = False
            cust_ord.caregiver = item['caregiver']
            cust_ord.date = datetime.strptime(item['date'], '%m/%d/%y').date()
            cust_ord.order_total = item['order_total'].lstrip('$')
            cust_ord.save()
            logger.info(u'Added {}'.format(str(cust_ord)))

        elif item['table_type'] == 'transaction':
            try:
                cust_ord = CustomerOrder.objects.get(order_id=item['order_id'],
                                                     customer__source_type=item['source_type'])
            except Customer.DoesNotExist:
                logger.error(u'There is no customer order #{}!'.format(item['order_id']))

            else:
                trans = Transaction()
                trans.order = cust_ord
                trans.description = item['description']
                trans.qty_dispensed = item['qty_dispensed']
                trans.qty_sold = item['qty_sold']
                trans.price = item['price'].lstrip('$')
                trans.subtotal = item['subtotal'].lstrip('$')
                trans.discount = item['discount']
                trans.tax = item['tax']
                trans.cashier = item['cashier']
                trans.save()
                logger.info(u'Added {}'.format(str(trans)))

        return item
