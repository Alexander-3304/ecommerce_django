from django.contrib import admin

from .models import Category, Item, ItemSize, ItemSale, ItemImage, ItemSet

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'new_price',
        'old_price',
        'stock',
        'available',
        'created_at',
        'updated_at',
    )
    list_filter = ('available', 'created_at', 'updated_at')
    list_editable = ('new_price', 'old_price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}


class ItemSaleAdmin(admin.ModelAdmin):
    list_display = (
        'product_sale',
        'sale_price',
        'sale_percent',
        'sale_begin',
        'sale_end',
    )
    list_filter = ('sale_begin', 'sale_end')
    list_editable = ('sale_price', 'sale_percent', 'sale_begin', 'sale_end')


class ItemSizeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'size')
    list_filter = ('category', 'size')
    list_editable = ('category', 'size')


class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image', 'alt', 'description')
    list_filter = ('alt', 'description', 'image')
    list_editable = ('alt', 'description', 'image')


class ItemSetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    list_filter = ('name', )
    list_editable = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemSale, ItemSaleAdmin)
admin.site.register(ItemSize, ItemSizeAdmin)
admin.site.register(ItemImage, ItemImageAdmin)
admin.site.register(ItemSet, ItemSetAdmin)