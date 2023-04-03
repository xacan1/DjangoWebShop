from rest_framework import serializers
from shop.models import *


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_staff', 'is_active',
                  'currency', 'price_type',)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class PriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceType
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
    price_type = PriceTypeSerializer(read_only=True)

    class Meta:
        model = Prices
        fields = '__all__'


class PriceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


# Сериализатор остатков на складах с детализацией по складам
class StockProductSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()

    class Meta:
        model = StockProducts
        fields = '__all__'


# для функции сохранения остатков
class StockProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProducts
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'external_code',
                  'photo', 'parent', 'nested_category',)


# тут нужен slug только для чтения для фронтэнда , где он используется для формирования поля
class ProductSerializer(serializers.ModelSerializer):
    get_prices = PriceSerializer(many=True, read_only=True)
    get_stock_product = StockProductSerializer(many=True, read_only=True)
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'external_code', 'category', 'photo',
                  'time_create', 'get_prices', 'get_stock_product', 'description',)


class ImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduct
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class AttributeValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValues
        fields = '__all__'


class AttributeProductValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeProductValues
        fields = '__all__'


class FavoriteProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = FavoriteProduct
        fields = '__all__'


class FavoriteProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = '__all__'


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
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


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


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
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
