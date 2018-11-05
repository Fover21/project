# __author: busensei
# data: 2018/10/29

from django.conf.urls import url
from django.contrib import admin
from crm.views import consultant
from crm.views import teacher

urlpatterns = [

    # 展示客户信息
    url(r'customer_list', consultant.Customer.as_view(), name='customer'),
    # 展示私户信息
    url(r'my_customer', consultant.Customer.as_view(), name='my_customer'),
    # 增加客户和编辑客户
    url(r'^customer/add/(?P<edit_id>\d+)', consultant.add_and_edit_customer, name='add_customer'),
    url(r'^customer/edit/(?P<edit_id>\d+)', consultant.add_and_edit_customer, name='edit_customer'),

]