from django.shortcuts import render, redirect, HttpResponse, reverse
from django.views import View
# Create your views here.


class Customer(View):

    def get(self, request):
        return render(request, 'crm/customer_list.html')