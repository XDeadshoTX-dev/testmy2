
from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = \
    ('Product_name', 'Product_stars', 'Product_available_quantity',
    'Product_single_price')
    search_fields = ('Product_name', 'Product_description')
    list_filter = (
    'Product_stars', 'Product_available_quantity', 'Product_single_price')
    ordering = ('Product_name',)
    fields = ('Product_name', 'Product_description', 'Product_image_url',
              'Product_image', 'Product_stars', 'Product_available_quantity',
              'Product_old_price', 'Product_single_price')
    readonly_fields = ('Product_id',)


admin.site.register(Product, ProductAdmin)
