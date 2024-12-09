from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext as __


class Product(models.Model):
    """
    Модель Product представляет собой товар, который можно продавать в интернет-магазине

    Заказы можно посмотреть тут: :model:`shopapp.Order`
    """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, verbose_name=_("Name"),
                            db_index=True)  # включаем индексацию для поиска по названию
    description = models.TextField(null=False, blank=True, verbose_name=_("Description"),
                                   db_index=True)  # включаем индексацию для поиска по описанию

    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_("Price"))
    discount = models.SmallIntegerField(default=0, verbose_name=_("Discount"))

    created_at = models.DateTimeField(auto_now_add=True)

    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['name', 'price']
        verbose_name = __("product")
        verbose_name_plural = __("products")

    def __str__(self):
        return _('Product, name={n}, id={p}').format(
            n=self.name,
            p=self.pk
        )


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('User'))

    delivery_address = models.TextField(null=True, blank=True, verbose_name=_('Delivery address'))
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name=_('Promocode'))
    created_at = models.DateTimeField(auto_now=True)

    products = models.ManyToManyField(Product, related_name="products", verbose_name=_('Products'))

    class Meta:
        verbose_name = __("order")
        verbose_name_plural = __("orders")

    def __str__(self):
        return _('Order №{pk} by {user}').format(
            pk=self.pk,
            user=self.user
        )
