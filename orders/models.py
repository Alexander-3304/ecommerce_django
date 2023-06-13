from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models
from .managers import OrderItemManager
from ustora_001.models import Item



# Create your models here.

class Order(models.Model):
    """Order model"""

    user = models.ForeignKey(verbose_name=_('Пользователь'), to=User, on_delete=models.SET_NULL, null=True, related_name='order_related_user',)

    # created_at = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=True)

    first_name = models.CharField(verbose_name=_('Имя'), max_length=50)
    last_name = models.CharField(verbose_name=_('Фамилия'), max_length=50)
    phone = models.CharField(verbose_name=_('Телефон'), max_length=28)
    email = models.EmailField(verbose_name=_('email'))
    address = models.CharField(verbose_name=_('Адрес'), max_length=250)
    postal_code = models.CharField(verbose_name=_('Индекс'), max_length=20)
    city = models.CharField(verbose_name=_('Город'), max_length=100)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'), auto_now_add=True)
    paid = models.BooleanField(verbose_name=_('Оплачен'), default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return  f'Order {self.pk}'

#OrderItem model
class OrderItem(models.Model):
    """Order model"""

    order = models.ForeignKey(verbose_name=_('Заказ'), to=Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(verbose_name=_('Товар'), to=Item, on_delete=models.CASCADE, related_name='order_items')

    price = models.DecimalField(verbose_name=_('Цена'), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name=_('Количество'))
    sale_percent = models.PositiveIntegerField(verbose_name=_('Процент скидки'), default=0)
    sale_price = models.DecimalField(verbose_name=_('Цена скидки'), max_digits=10, decimal_places=2, blank=True, null=True)

    objects = models.Manager()
    items = OrderItemManager()

    class Meta:
        verbose_name = _('Товар в заказе')
        verbose_name_plural = _('Товары в заказе')

    def __str__(self):
        return  f'Order {self.order.pk}'

    def total_price(self):
        total = self.price * self.quantity
        return total


