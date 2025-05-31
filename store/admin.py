from django.contrib import admin

from .models import Category, Color, Features, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    ordering = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','main_price','price_with_discount','inventory','is_special_offer','date_time_added',]
    search_fields = ['name', 'category__title']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'category']
    readonly_fields = ['date_time_added', 'ate_time_modified']

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ['product', 'weight', 'size', ]

admin.site.register(Color)