from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.admin import TokenAdmin
from .models import *

TokenAdmin.raw_id_fields = ['user']


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'phone', 'last_name', 'first_name',
                    'last_login', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    list_editable = ('is_staff', 'is_active',)
    list_display_links = ('email', 'phone', 'last_name', 'first_name',)
    fieldsets = (
        (None, {'fields': ('email', 'password',
         'phone', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone',
                       'first_name', 'last_name', 'is_staff', 'is_active',)}
         ),
    )
    search_fields = ('email', 'phone', 'last_name',)
    ordering = ('email',)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'external_code',)
    list_display_links = ('name',)
    search_fields = ('name', 'external_code',)
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'photo', 'category',
                    'is_published', 'external_code',)
    list_filter = ('category', 'is_published',)
    search_fields = ('name', 'external_code',)
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('name',)}


class PricesAdmin(admin.ModelAdmin):
    model = Prices
    list_display = ('product', 'price', 'date_update', 'discount_percentage',)
    list_filter = ('date_update',)


class AttributeCategoryAdmin(admin.ModelAdmin):
    model = AttributeCategory
    list_display = ('category', 'attribute',)


class AttributeProductAdmin(admin.ModelAdmin):
    model = AttributeProduct
    list_display = ('product', 'attribute', 'value',)


class WarehouseAdmin(admin.ModelAdmin):
    model = Warehouse
    list_display = ('name', 'country', 'province',
                    'city', 'address', 'external_code',)
    search_fields = ('name', 'country', 'province',
                     'city', 'address', 'external_code',)


class StockProductsAdmin(admin.ModelAdmin):
    model = StockProducts
    list_display = ('product', 'stock', 'warehouse',)
    list_filter = ('warehouse',)


class CartProductAdmin(admin.ModelAdmin):
    model = CartProduct
    list_display = ('user', 'cart', 'product', 'quantity', 'price', 'discount',
                    'discount_percentage', 'amount', 'warehouse', 'id_anonymous',)
    list_display_links = ('user',)
    list_filter = ('user',)
    search_fields = ('id_anonymous',)


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('user', 'quantity', 'amount', 'discount',
                    'in_order', 'for_anonymous_user',)
    list_filter = ('in_order', 'for_anonymous_user',)


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('castomer', 'phone', 'status',
                    'buying_type', 'number', 'id_anonymous',)
    list_filter = ('status', 'buying_type', 'time_create',)
    search_fields = ('castomer', 'phone', 'number',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Attribute, admin.ModelAdmin)
admin.site.register(AttributeCategory, AttributeCategoryAdmin)
admin.site.register(AttributeProduct, AttributeProductAdmin)
admin.site.register(Prices, PricesAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(StockProducts, StockProductsAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
