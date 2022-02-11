from django.shortcuts import render
from datetime import datetime
import json

# Create your views here.
with open('context.json', 'r', encoding='utf-8') as f:
   contex_json = json.load(f)

mainapp_list = contex_json['mainapp_list']

def index(request):
    return render(request, 'mainapp/index.html', context={
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
    })


def products(request):
    products_category = contex_json['products_category']
    return render(request, 'mainapp/products.html', context={
        'products_category': products_category,
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
    })


def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
    })