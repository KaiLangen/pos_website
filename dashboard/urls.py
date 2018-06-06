from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/cust', views.CustomerList.as_view(), name='api_cust'),
    url(r'^api/orders', views.CustomerOrderList.as_view(), name='api_orders'),
    url(r'^api/trans', views.TransactionList.as_view(), name='api_trans'),
    url(r'^login/', views.login, {'template_name': 'admin/login.html', 'redirect_authenticated_user': True},
        name='login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
