from cartapp.models import Cart


def cart(request):
    cart = []

    if request.user.is_authenticated:
        cart = request.user.cart.select_related()


    return {
        'cart' : cart
    }