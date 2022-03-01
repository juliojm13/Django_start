from django.shortcuts import render, HttpResponseRedirect,get_object_or_404
from cartapp.models import Cart
from mainapp.models import Product


def cart(request):
    cart = Cart.objects.filter(user = request.user)
    context = {'cart' : cart}
    return render(request,'cartapp/cart.html',context)



def add_to_cart(request, pk):
    # import pdb; pdb.set_trace()
    product = get_object_or_404(Product, pk=pk)

    cart_product = Cart.objects.filter(user=request.user, product=product).first()

    if not cart_product:
        cart_product = Cart(user=request.user, product=product)

    cart_product.quantity += 1
    cart_product.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request):
    pass


