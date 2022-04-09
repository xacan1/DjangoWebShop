from rest_framework import serializers
from .models import *


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'is_staff', 'is_active',)


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('price', 'date_update', 'discount_percentage',)


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ('pk', 'name', 'city', 'external_code',)


# Сериализатор остатков на складах с детализацией по складам
class StockProductSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()

    class Meta:
        model = StockProducts
        fields = ('warehouse', 'stock',)


class ProductSerializer(serializers.ModelSerializer):
    get_prices = PriceSerializer(many=True, read_only=True)
    get_stock_product = StockProductSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('pk', 'name', 'external_code', 'photo', 'time_create',
                  'get_prices', 'get_stock_product',)


class CategorySerializer(serializers.ModelSerializer):
    # get_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


# Сериализатор строки Корзины для просмотра данных с детализацией по товару и складу
class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    warehouse = WarehouseSerializer()

    class Meta:
        model = CartProduct
        fields = '__all__'


# Сериализатор строки Корзины для записи новой строки Корзины, тут не нужно детализировать товар и склад, достаточно указать их pk
class CartProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    get_cart_products = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('pk', 'user', 'get_cart_products', 'quantity',
                  'amount', 'discount', 'in_order', 'for_anonymous_user',)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    # EXAMPLES:
    # qs = StockProducts.objects.select_related(
    #     'warehouse').select_related('product').filter(product__category=1)
    # print(qs)
    # print(qs.query)
    # print(StockProductSerializer(qs, many=True).data)
