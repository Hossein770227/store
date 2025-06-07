from django.contrib import admin

from orders.models import Order, OrderItems


class OrderItemsInLine(admin.TabularInline):
    model = OrderItems
    fields = ['product', 'quantity', 'price', ]
    extra = 0




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'is_paid']
    list_filter = ['user', 'first_name', 'last_name', 'is_paid']
    search_fields = ['user', 'first_name', 'last_name',]
    inlines = [OrderItemsInLine]