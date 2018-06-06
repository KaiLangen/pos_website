from __future__ import unicode_literals
from django.db import models


class Customer(models.Model):
    source_type = models.CharField(max_length=100)
    source_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    bucket = models.CharField(max_length=1)

    def __str__(self):
        return ('source_type = {}   '
                'source_id = {}   '
                'name = {}   '
                'bucket = {}   ').format(self.source_type,
                                         self.source_id,
                                         self.name,
                                         self.bucket)


class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    member = models.BooleanField()
    caregiver = models.CharField(max_length=100)
    date = models.DateField()
    order_total = models.FloatField()

    def __str__(self):
        return ('source_type = {}   '
                'source_id = {}   '
                'name = {}   '
                'order_id = {}   '
                'member = {}   '
                'caregiver = {}   '
                'date = {}   '
                'order_total = {}   ').format(self.customer.source_type,
                                              self.customer.source_id,
                                              self.customer.name,
                                              self.order_id,
                                              self.member,
                                              self.caregiver,
                                              self.date,
                                              self.order_total)


class Transaction(models.Model):
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    qty_dispensed = models.CharField(max_length=100)
    qty_sold = models.CharField(max_length=100)
    price = models.FloatField()
    subtotal = models.FloatField()
    discount = models.CharField(max_length=100)
    tax = models.CharField(max_length=100)
    cashier = models.CharField(max_length=100)

    def __str__(self):
        return ('source_type = {}   '
                'source_id = {}   '
                'name = {}   '
                'order_id = {}   '
                'date = {}   '
                'description = {}   '
                'qty_dispensed = {}   '
                'qty_sold = {}   '
                'price = {}   '
                'subtotal = {}   '
                'discount = {}   '
                'tax = {}   '
                'cashier = {}   ').format(self.order.customer.source_type,
                                          self.order.customer.source_id,
                                          self.order.customer.name,
                                          self.order.order_id,
                                          self.order.date,
                                          self.description,
                                          self.qty_dispensed,
                                          self.qty_sold,
                                          self.price,
                                          self.subtotal,
                                          self.discount,
                                          self.tax,
                                          self.cashier)
