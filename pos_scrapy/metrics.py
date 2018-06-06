import logging
from datetime import datetime, timedelta
from django.db.models import Sum

logger = logging.getLogger('metrics')

DATE_LAST_MONTH = (datetime.now() - timedelta(31)).date()


def calculate_aov(orders):
    amount_per_month = orders.aggregate(Sum('order_total'))['order_total__sum']
    orders_per_month = orders.count()

    if amount_per_month and orders_per_month:
        return amount_per_month / orders_per_month
    else:
        return 0


def calculate_frequency(orders):
    frequency = 0
    for order in orders:
        frequency += order.transaction_set.count()
    return frequency


def calculate_ltov(cust):
    return cust.customerorder_set.all().aggregate(Sum('order_total'))['order_total__sum']


def calculate_metrics(cust):
    orders = cust.customerorder_set.filter(date__gte=DATE_LAST_MONTH)
    aov = calculate_aov(orders)
    frequency = calculate_frequency(orders)
    ltov = calculate_ltov(cust)

    if aov > 1000 and frequency > 100:
        cust.bucket = 'P'
    elif aov > 500:
        cust.bucket = 'D'
    elif frequency > 25:
        cust.bucket = 'G'
    elif ltov > 250:
        cust.bucket = 'S'
    else:
        cust.bucket = 'B'

    cust.save()
    logger.info(u'Modified bucket {}'.format(str(cust)))
