import jdatetime
from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Order, OrderItems


class OrderItemsInLine(admin.TabularInline):
    model = OrderItems
    fields = ['product', 'quantity', 'price', ]
    extra = 0




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'is_paid', 'date_time_persian']
    list_filter = ['user', 'first_name', 'last_name', 'is_paid']
    search_fields = ['user', 'first_name', 'last_name',]
    inlines = [OrderItemsInLine]

    def date_time_persian(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.date_time_created).strftime("%Y/%m/%d %H:%M:%S")

    date_time_persian.short_description = _('date time')
    date_time_persian.admin_order_field =  _('date time')