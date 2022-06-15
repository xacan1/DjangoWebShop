from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.admin import TokenAdmin
from .models import *

TokenAdmin.raw_id_fields = ['user']


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'phone', 'last_name', 'first_name', 'currency',
                    'price_type', 'last_login', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    list_editable = ('is_staff', 'is_active',)
    list_display_links = ('email', 'phone', 'last_name', 'first_name',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone', 'first_name',
                           'last_name', 'currency', 'price_type',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone', 'first_name', 'last_name',
                       'is_staff', 'is_active', 'currency', 'price_type',)}
         ),
    )
    search_fields = ('email', 'phone', 'last_name',)
    ordering = ('email',)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('parent', 'name', 'external_code',)
    list_display_links = ('name',)
    search_fields = ('name', 'external_code',)
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'photo', 'category', 'is_service',
                    'is_published', 'external_code',)
    list_filter = ('category', 'is_published', 'is_service',)
    search_fields = ('name', 'external_code',)
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('name',)}


class FavoriteProductAdmin(admin.ModelAdmin):
    model = FavoriteProduct
    list_display = ('user', 'product', 'id_messenger',)
    list_display_links = ('user', 'product',)
    search_fields = ('user__email', 'product__name', 'id_messenger',)


class CurrencyAdmin(admin.ModelAdmin):
    model = Currency
    list_display = ('name', 'abbreviation', 'digital_code', 'sign', 'default',)
    list_display_links = ('name', 'abbreviation', 'digital_code', 'sign',)
    list_editable = ('default',)
    search_fields = ('name', 'digital_code',)


class PriceTypeAdmin(admin.ModelAdmin):
    model = PriceType
    list_display = ('name', 'external_code', 'default',)
    list_display_links = ('name',)
    list_editable = ('default',)
    search_fields = ('name', 'external_code',)


class PricesAdmin(admin.ModelAdmin):
    model = Prices
    list_display = ('product', 'price', 'date_update', 'discount_percentage',
                    'currency', 'price_type',)
    list_filter = ('date_update',)
    search_fields = ('product__name',)


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
    list_display = ('user', 'cart', 'order', 'product', 'quantity', 'price', 'discount',
                    'discount_percentage', 'amount', 'warehouse', 'phone', 'id_messenger',)
    list_display_links = ('user', 'order',)
    search_fields = ('phone', 'id_messenger', 'amount', 'user__email',)


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('user', 'quantity', 'amount',
                    'discount', 'for_anonymous_user',)
    list_filter = ('for_anonymous_user',)
    search_fields = ('user__email',)


class StatusAdmin(admin.ModelAdmin):
    model = Status
    list_display = ('name', 'repr', 'for_bot', 'use',)
    list_filter = ('use', 'for_bot',)


class PaymentTypeAdmin(admin.ModelAdmin):
    model = Status
    list_display = ('name', 'repr', 'for_bot', 'use',)
    list_filter = ('use', 'for_bot',)


class DeliveryTypeAdmin(admin.ModelAdmin):
    model = Status
    list_display = ('name', 'repr', 'for_bot', 'use',)
    list_filter = ('use', 'for_bot',)


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('pk', 'user', 'phone', 'status', 'delivery_date', 'delivery_type',
                    'paid', 'quantity', 'amount', 'discount', 'number', 'time_create',)
    list_display_links = ('pk', 'user', 'phone', 'status',)
    list_filter = ('status', 'delivery_type',
                   'payment_type', 'paid', 'time_create',)
    search_fields = ('user', 'phone', 'number',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)
admin.site.register(Attribute, admin.ModelAdmin)
admin.site.register(AttributeCategory, AttributeCategoryAdmin)
admin.site.register(AttributeProduct, AttributeProductAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(PriceType, PriceTypeAdmin)
admin.site.register(Prices, PricesAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(StockProducts, StockProductsAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(PaymentType, PaymentTypeAdmin)
admin.site.register(DeliveryType, DeliveryTypeAdmin)
admin.site.register(Order, OrderAdmin)
