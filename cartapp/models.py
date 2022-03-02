from django.db import models
from django.conf import settings
from mainapp.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='Время', auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def product_total_cost(self):
        "return the total cost of the same product"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        "return the total quantity of products on cart"
        _user_cart = Cart.objects.filter(user = self.user)
        _total_quantity = sum(item.quantity for item in _user_cart)
        return _total_quantity

    @property
    def total_cost(self):
        "return the total cost of products on cart"
        _user_cart = Cart.objects.filter(user = self.user)
        _total_cost = sum(item.product.price*item.quantity for item in _user_cart)
        return _total_cost