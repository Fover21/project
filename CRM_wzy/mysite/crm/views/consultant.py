from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import auth
from crm import forms
from django.views import View
from django.db.models import Q
from crm import models
from utils.pagination import Pagination
from django.http import QueryDict
from django.utils.safestring import mark_safe
# Create your views here.


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        obj = auth.authenticate(username=username, password=password)
        print(obj)
        if obj:
            auth.login(request, obj)
            return redirect(reverse('crm:customer'))
    return render(request, 'login.html')


# 注册
def register(request):
    # 拿到数据库中字段对应的值（ModelForm）普通不与数据库相连的是Form
    form_obj = forms.RegisterForms()
    if request.method == 'POST':
        form_obj = forms.RegisterForms(request.POST)
        if form_obj.is_valid():
            # 方式一
            # print('form_obj.cleaned_data', form_obj.cleaned_data)
            # form_obj.cleaned_data.pop('re_password')
            # models.UserProfile.objects.create_user(**form_obj.cleaned_data)
            # 方式二
            obj = form_obj.save()  # 直接将原数据存入数据库
            # 但是密码需要进行加密，所有需要设置加密后的密码
            pwd = obj.password
            print(pwd)
            obj.set_password(pwd)
            obj.save()
            return redirect(reverse('login'))
    return render(request, 'register.html', {"form_obj": form_obj})


# 注销
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


# 展示客户信息
class Customer(View):
    def get(self, request):
        # 查询条件
        q = self.get_search_content(['qq', 'name'])
        if self.request.path_info == reverse('crm:my_customer'):
            # 用户表的销售为当前登录的用户表示私户
            customer = models.Customer.objects.filter(q, consultant=request.user)
        else:
            # 没有分配销售的为公户
            customer = models.Customer.objects.filter(q, consultant__isnull=True)
        # 解决搜索后的url翻页拼接问题
        query_params = self.request.GET.copy()
        page = Pagination(request, customer.count(), query_params)
        # 生成添加按钮
        add_btn, query_params = self.get_add_btn()
        return render(request, 'crm/consultant/customer_list.html',{
            "customer": customer[page.start: page.end],
            "html_str": page.show_li,
            "add_btn": add_btn,
            "query_params": query_params,
        })

    def get_search_content(self, fields_list):
        # 获取查询框中的数据，找不到给一个默认值，否则会报错
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for i in fields_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q

    # 生成添加按钮
    def get_add_btn(self):
        # 获取添加按钮
        url = self.request.get_full_path()

        qd = QueryDict()
        qd._mutable = True
        qd['next'] = url
        query_params = qd.urlencode()
        add_btn = '<a href="{}?{}" class="btn btn-primary btn-sm" style="margin-bottom: 10px">添加</a>'.format(
            reverse('crm:add_customer', args=(0, )), query_params)
        return mark_safe(add_btn), query_params


# 添加和编辑用户
def add_and_edit_customer(request, edit_id=None):
    obj = models.Customer.objects.filter(id=edit_id).first()
    form_obj = forms.CustomerForm(instance=obj)
    title = '编辑用户' if edit_id != '0' else '添加用户'
    if request.method == 'POST':
        form_obj = forms.CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            # 创建一个新的数据或修改原始数据
            form_obj.save()
            # 获取next
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect(reverse('crm:customer'))
    return render(request, 'crm/forms.html', {
        "form_obj": form_obj,
        'title': title
    })