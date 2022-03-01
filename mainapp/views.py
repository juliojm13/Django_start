from django.shortcuts import render
from datetime import datetime
import json
from .models import ProductCategory, Product

# Create your views here.
with open('context.json', 'r', encoding='utf-8') as f:
   contex_json = json.load(f)

mainapp_list = contex_json['mainapp_list']

def index(request):
    cart = []
    if request.user.is_authenticated:
        cart = request.user.cart.all()
    total_products_in_cart = 0
    total_cost_in_cart = 0
    for el in cart:
        total_products_in_cart += el.quantity
        total_cost_in_cart += el.product.price * el.quantity
    products = Product.objects.all()[:2]
    return render(request, 'mainapp/index.html', context={
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        'products': products,
        'cart':cart,
        'total_products_in_cart':total_products_in_cart,
        'total_cost_in_cart':total_cost_in_cart
    })


def products(request):
    products_category = ProductCategory.objects.all()
    cart =[]
    if request.user.is_authenticated:
        cart= request.user.cart.all()
    total_products_in_cart = 0
    total_cost_in_cart = 0
    for el in cart:
        total_products_in_cart += el.quantity
        total_cost_in_cart += el.product.price * el.quantity
    return render(request, 'mainapp/products.html', context={
        'products_category': products_category,
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        'cart': cart,
        'total_products_in_cart':total_products_in_cart,
        'total_cost_in_cart':total_cost_in_cart
    })


def contact(request):
    cart = []
    if request.user.is_authenticated:
        cart = request.user.cart.all()
    total_products_in_cart = 0
    total_cost_in_cart = 0
    for el in cart:
        total_products_in_cart += el.quantity
        total_cost_in_cart += el.product.price * el.quantity
    return render(request, 'mainapp/contact.html', context={
        'mainapp_list': mainapp_list,
        'now_date': datetime.now(),
        'name': 'jarno',
        'cart':cart,
        'total_products_in_cart':total_products_in_cart,
        'total_cost_in_cart':total_cost_in_cart
    })


def products_category(request, pk = None):
    # import pdb; pdb.set_trace()
    products_category = ProductCategory.objects.all()
    cart =[]
    if request.user.is_authenticated:
        cart= request.user.cart.all()
    total_products_in_cart = 0
    total_cost_in_cart = 0
    for el in cart:
        total_products_in_cart += el.quantity
        total_cost_in_cart += el.product.price * el.quantity
    if pk is None:
        products_of_category = Product.objects.all()
    else:
        products_of_category = Product.objects.filter(category_id=pk)
    return render(request, 'mainapp/products_category.html',context={
        'products_of_category':products_of_category,
        'mainapp_list': mainapp_list,
        'products_category': products_category,
        'selected_category_id': pk,
        'cart': cart,
        'total_products_in_cart':total_products_in_cart,
        'total_cost_in_cart':total_cost_in_cart
    })