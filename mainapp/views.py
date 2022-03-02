from django.shortcuts import render
from datetime import datetime
import json
from .models import ProductCategory, Product
import random

# Create your views here.
with open('context.json', 'r', encoding='utf-8') as f:
    contex_json = json.load(f)

mainapp_list = contex_json['mainapp_list']


def get_cart(user):
    if user.is_authenticated:
        return user.cart.all()
    else:
        return []


def get_hot_product():
    products = Product.objects.all()

    return random.choice(products)


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category). \
                        exclude(pk=hot_product.pk)[:3]

    return same_products


def index(request):
    cart = get_cart(request.user)
    products = Product.objects.all()[:4]
    return render(request, 'mainapp/index.html', context={
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        'products': products,
        'cart': cart,
    })


def products(request):
    products_category = ProductCategory.objects.all()
    cart = get_cart(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    return render(request, 'mainapp/products.html', context={
        'products_category': products_category,
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        'cart': cart,
        'hot_product': hot_product,
        'same_products': same_products
    })


def contact(request):
    cart = get_cart(request.user)
    return render(request, 'mainapp/contact.html', context={
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        'cart': cart,
    })


def products_category(request, pk=None):
    # import pdb; pdb.set_trace()
    products_category = ProductCategory.objects.all()
    cart = get_cart(request.user)
    if pk is None:
        products_of_category = Product.objects.all()
    else:
        products_of_category = Product.objects.filter(category_id=pk)
    return render(request, 'mainapp/products_category.html', context={
        'products_of_category': products_of_category,
        'mainapp_list': mainapp_list,
        'products_category': products_category,
        'selected_category_id': pk,
        'cart': cart,
    })
