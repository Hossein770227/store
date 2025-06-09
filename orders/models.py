from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email"), max_length=254, blank=True, null=True)
    address = models.CharField(_("address"), max_length=500)
    order_notes = models.TextField(_("order notes"), blank=True, null=True)
    is_paid = models.BooleanField(_("is paid?"), default=False)
    date_time_created = models.DateTimeField(_("date time created"), auto_now_add=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.date_time_created}"
    

class OrderItems(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("order"), on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey("store.Product", verbose_name=_("product"), on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveSmallIntegerField(_("quantity"), default=1)
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = _("order items")
        verbose_name_plural = _("order items")

    def get_total_price(self):
        return self.quantity * self.price
    

    def __str__(self):
        return f"{self.product} - {self.quantity}"
    