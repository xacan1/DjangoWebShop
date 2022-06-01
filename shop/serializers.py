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
        fields = ('pk', 'product', 'price',
                  'date_update', 'discount_percentage',)


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ('pk', 'name', 'country', 'province',
                  'city', 'address', 'external_code',)


# Сериализатор остатков на складах с детализацией по складам
class StockProductSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()

    class Meta:
        model = StockProducts
        fields = ('pk', 'warehouse', 'stock',)


# для функции сохранения остатков
class StockProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProducts
        fields = ('product', 'warehouse', 'stock',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'external_code', 'parent', 'nested_category',)


class ProductSerializer(serializers.ModelSerializer):
    get_prices = PriceSerializer(many=True, read_only=True)
    get_stock_product = StockProductSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('pk', 'name', 'external_code', 'category', 'photo',
                  'time_create', 'get_prices', 'get_stock_product', 'description',)


# Сериализатор строки Корзины для просмотра данных с детализацией по товару и складу
class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

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
                  'amount', 'discount', 'for_anonymous_user',)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'


class DeliveryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryType
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    delivery_type = DeliveryTypeSerializer(read_only=True)
    payment_type = PaymentTypeSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


# для создания заказа без лишних сериализаций
class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    # EXAMPLES:
    # qs = StockProducts.objects.select_related(
    #     'warehouse').select_related('product').filter(product__category=1)
    # print(qs)
    # print(qs.query)
    # print(StockProductSerializer(qs, many=True).data)
