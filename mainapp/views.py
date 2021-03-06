from django.shortcuts import render, get_object_or_404
from datetime import datetime
import json
from .models import ProductCategory, Product
import random
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
with open('context.json', 'r', encoding='utf-8') as f:
    contex_json = json.load(f)

mainapp_list = contex_json['mainapp_list']


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
            return links_menu
        else:
            return ProductCategory.objects.filter(is_active=True)

def get_categories():
    if settings.LOW_CACHE:
        key = f'categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductCategory.objects.all().filter(is_active=True)
            cache.set(key, categories)
            return categories
        else:
            return ProductCategory.objects.all().filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
            return category
        else:
            return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
            return products
        else:
            return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
            return product
        else:
            return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
            return products
        else:
            return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
            return products
        else:
            return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_cart(user):
    if user.is_authenticated:
        return user.cart.all()
    else:
        return []


def get_hot_product():
    products = get_products()

    return random.choice(products)


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category). \
                        exclude(pk=hot_product.pk).filter(is_active=True)[:3]

    return same_products


def index(request):
    cart = get_cart(request.user)
    products = get_products()[:4]
    return render(request, 'mainapp/index.html', context={
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        'products': products,
        # 'cart': cart,
    })


def products(request):
    products_category = get_categories()
    cart = get_cart(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    return render(request, 'mainapp/products.html', context={
        'products_category': products_category,
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        # 'cart': cart,
        'hot_product': hot_product,
        'same_products': same_products,
    })


def contact(request):
    cart = get_cart(request.user)
    return render(request, 'mainapp/contact.html', context={
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        # 'cart': cart,
    })


def products_category(request, pk=None, page=1):
    products_category = get_categories()
    if pk is None:
        products_of_category = get_products()
    else:
        products_of_category = get_products_in_category_orederd_by_price(pk)

    paginator = Paginator(products_of_category, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    return render(request, 'mainapp/products_category.html', context={
        'products_of_category': products_paginator,
        'mainapp_list': mainapp_list,
        'products_category': products_category,
        'selected_category_id': pk,
        # 'cart': cart,
    })
