from django.shortcuts import render
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login)
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView
from rest_framework.response import Response
from serializers import CustomerSerializer, CustomerOrderSerializer, TransactionSerializer
from models import Customer, CustomerOrder, Transaction


def index(request):
    if request.user.is_authenticated:
        context = dict()

        context['data_customers'] = list()
        for entry in Customer.objects.all():
            temp_dict = dict()
            temp_dict['source_type'] = entry.source_type
            temp_dict['source_id'] = entry.source_id
            temp_dict['name'] = entry.name
            temp_dict['bucket'] = entry.bucket
            context['data_customers'].append(temp_dict)

        context['data_customer_orders'] = list()
        for entry in CustomerOrder.objects.all():
            temp_dict = dict()
            temp_dict['source_type'] = entry.customer.source_type
            temp_dict['source_id'] = entry.customer.source_id
            temp_dict['name'] = '{} {}'.format(entry.customer.name, entry.customer.bucket)
            temp_dict['order_id'] = entry.order_id
            temp_dict['member'] = entry.member
            temp_dict['caregiver'] = entry.caregiver
            temp_dict['date'] = entry.date
            temp_dict['order_total'] = entry.order_total
            context['data_customer_orders'].append(temp_dict)

        context['data_transactions'] = list()
        for entry in Transaction.objects.all():
            temp_dict = dict()
            temp_dict['source_type'] = entry.order.customer.source_type
            temp_dict['source_id'] = entry.order.customer.source_id
            temp_dict['name'] = '{} {}'.format(entry.order.customer.name, entry.order.customer.bucket)
            temp_dict['order_id'] = entry.order.order_id
            temp_dict['date'] = entry.order.date
            temp_dict['description'] = entry.description
            temp_dict['qty_dispensed'] = entry.qty_dispensed
            temp_dict['qty_sold'] = entry.qty_sold
            temp_dict['price'] = entry.price
            temp_dict['subtotal'] = entry.subtotal
            temp_dict['discount'] = entry.discount
            temp_dict['tax'] = entry.tax
            temp_dict['cashier'] = entry.cashier
            context['data_transactions'].append(temp_dict)

        return render(request, 'dashboard/index.html', context)
    else:
        return HttpResponseRedirect('/login/')


def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None, redirect_authenticated_user=False):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, '/'))

    if redirect_authenticated_user and request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to)
    elif request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


class CustomerList(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseRedirect('/login/')


class CustomerOrderList(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            orders = CustomerOrder.objects.all()
            serializer = CustomerOrderSerializer(orders, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseRedirect('/login/')


class TransactionList(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            transactions = Transaction.objects.all()
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseRedirect('/login/')
