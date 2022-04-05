from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.db import transaction


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
        _user_cart = Cart.objects.filter(user=self.user)
        _total_quantity = sum(item.quantity for item in _user_cart)
        return _total_quantity

    @property
    def total_cost(self):
        "return the total cost of products on cart"
        _user_cart = Cart.objects.filter(user=self.user)
        _total_cost = sum(item.product.price * item.quantity for item in _user_cart)
        return _total_cost

    @staticmethod
    def get_item(pk):
        return Cart.objects.filter(id=pk).first()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
            else:
                self.product.quantity -= self.quantity
            self.product.save()
            super(Cart, self).save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):

        self.product.quantity += self.quantity  # giving back to the storage after canceling the order
        self.product.save()
        super(self.__class__, self).delete(*args, **kwargs)
