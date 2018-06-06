# -*- coding: utf-8 -*-

import scrapy


class CustomerOrder(scrapy.Item):
    table_type = scrapy.Field()
    source_type = scrapy.Field()
    source_id = scrapy.Field()
    name = scrapy.Field()
    order_id = scrapy.Field()
    member = scrapy.Field()
    caregiver = scrapy.Field()
    date = scrapy.Field()
    order_total = scrapy.Field()


class Transaction(scrapy.Item):
    table_type = scrapy.Field()
    source_type = scrapy.Field()
    name = scrapy.Field()
    order_id = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    qty_dispensed = scrapy.Field()
    qty_sold = scrapy.Field()
    price = scrapy.Field()
    subtotal = scrapy.Field()
    discount = scrapy.Field()
    tax = scrapy.Field()
    cashier = scrapy.Field()
