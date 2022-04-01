from django.db import models
from django.conf import settings
from mainapp.models import Product


class Order(models.Model):
    FORMING = 1
    SENT_TO_PROCEED = 2
    PAID = 3
    PROCEED = 4
    READY = 5
    CANCEL = 6

    ORDER_STATUSES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'В обработке'),
        (PAID, 'Оплачен'),
        (PROCEED, 'Собирается'),
        (READY, 'Готов'),
        (CANCEL, 'Отменен'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='время изменения', auto_now=True)
    status = models.PositiveIntegerField(choices=ORDER_STATUSES, verbose_name='статус', default=FORMING)
    is_active = models.BooleanField(verbose_name='Активен ли', default=True)

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    @property
    def get_total_cost(self):
        items = self.items.select_related()
        return sum(list(map(lambda x: x.cost, items)))

    @property
    def get_total_quantity(self):
        items = self.items.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def delete(self, using=None, keep_parents=False):
        for item in self.items.select_related():
            item.product.quantity += item.quantity  # giving back to the storage after canceling the order
            item.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    @property
    def cost(self):
        return self.product.price * self.quantity
