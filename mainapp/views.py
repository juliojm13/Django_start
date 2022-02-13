from django.shortcuts import render
from datetime import datetime
import json
from .models import ProductCategory, Product

# Create your views here.
with open('context.json', 'r', encoding='utf-8') as f:
   contex_json = json.load(f)

mainapp_list = contex_json['mainapp_list']

def index(request):
    products = Product.objects.all()[:2]
    return render(request, 'mainapp/index.html', context={
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        'products': products
    })


def products(request):
    products_category = ProductCategory.objects.all()
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


def products_category(request, pk = None):
    products_category = ProductCategory.objects.all()
    products_of_category = Product.objects.filter(category_id=pk)
    return render(request, 'mainapp/products_category.html',context={
        'products_of_category':products_of_category,
        'mainapp_list': mainapp_list,
        'products_category': products_category,
        'selected_category_id': pk
    })