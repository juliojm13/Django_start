from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, reverse
from cartapp.models import Cart
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required()
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    # context = {'cart': cart}
    return render(request, 'cartapp/cart.html')


@login_required()
def add_to_cart(request, pk):
    # import pdb; pdb.set_trace()
    product = get_object_or_404(Product, pk=pk)

    cart_product = Cart.objects.filter(user=request.user, product=product).first()

    if not cart_product:
        cart_product = Cart(user=request.user, product=product)

    cart_product.quantity += 1
    cart_product.save()

    return HttpResponseRedirect(reverse('cart:adding_product', args=[pk]))


@login_required()
def remove_from_cart(request, pk):
    selected_product = get_object_or_404(Cart, pk=pk)
    selected_product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def adding_product(request, pk):
    mainapp_list = [{"view_name": "index", "link_name": "домой"},
                    {"view_name": "products:index", "link_name": "Продукты"},
                    {"view_name": "contact", "link_name": "Контакты"}]
    cart = Cart.objects.filter(user=request.user)
    selected_product = get_object_or_404(Product, pk=pk)
    products_category = ProductCategory.objects.all()
    context = {'selected_product': selected_product,
               'products_category': products_category,
               'cart': cart,
               'mainapp_list': mainapp_list,
               }
    return render(request, 'cartapp/selected_product.html', context)


@login_required
def cart_edit(request, pk, quantity):

    quantity = int(quantity)
    new_cart_item = Cart.objects.get(pk=int(pk))

    if quantity > 0:
        new_cart_item.quantity = quantity
        new_cart_item.save()
    else:
        new_cart_item.delete()

    cart = Cart.objects.filter(user=request.user)
    content = {
        'cart': cart,
    }

    result = render_to_string('cartapp/includes/inc_cart_list.html', \
                                  content)

    return JsonResponse({'result': result})
