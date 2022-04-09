from django.views.generic import ListView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *


class IndexView(ListView):
    model = Category
    template_name = 'shop/index.html'


class TokensAPIList(generics.ListAPIView):
    serializer_class = TokenSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        token = self.request.headers.get('authorization', 'error')
        token = token.replace('Token ', '')
        queryset = Token.objects.filter(key=token)
        return queryset


class UsersAPIRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'
    permission_classes = (IsAuthenticated,)


class CategoryAPIList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class CategoryAPICreate(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class CategoryAPIRetrieve(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'external_code'
    permission_classes = (IsAuthenticated,)


class CategoryAPIUpdate(generics.UpdateAPIView):
    queryset = Category.objects.all()
    lookup_field = 'external_code'
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class CategoryAPIDelete(generics.DestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'external_code'
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


# Параметры:
# category_pk - категория товара (каталог)
# warehouse_pk - склад
# Выводит список товаров с остатками по складам и ценами
class ProductAPIList(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # self.request.data - данные POST запроса
        # self.request.query_params - данные GET запроса
        category_pk = self.request.query_params.get('category_pk', 0)
        warehouse_pk = self.request.query_params.get('warehouse_pk', 0)

        if category_pk and warehouse_pk:
            queryset = Product.objects.filter(
                category=category_pk, get_stock_product__warehouse=warehouse_pk)
        elif category_pk:
            queryset = Product.objects.filter(category=category_pk)
        elif warehouse_pk:
            queryset = Product.objects.filter(
                get_stock_product__warehouse=warehouse_pk)
        else:
            queryset = Product.objects.all()

        return queryset


class ProductAPICreate(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)


class ProductAPIRetrieve(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    lookup_field = 'external_code'
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ProductAPIUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    lookup_field = 'external_code'
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)


class ProductAPIDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'external_code'
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)


class WarehouseAPIList(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = (IsAuthenticated,)


class WarehouseAPICreate(generics.CreateAPIView):
    serializer_class = WarehouseSerializer
    permission_classes = (IsAdminUser,)


class WarehouseAPIRetrieve(generics.RetrieveAPIView):
    queryset = Warehouse.objects.all()
    lookup_field = 'external_code'
    serializer_class = WarehouseSerializer
    permission_classes = (IsAuthenticated,)


class WarehouseAPIUpdate(generics.UpdateAPIView):
    queryset = Warehouse.objects.all()
    lookup_field = 'external_code'
    serializer_class = WarehouseSerializer
    permission_classes = (IsAdminUser,)


class WarehouseAPIDelete(generics.DestroyAPIView):
    queryset = Warehouse.objects.all()
    lookup_field = 'external_code'
    serializer_class = WarehouseSerializer
    permission_classes = (IsAdminUser,)


class PricesAPIList(generics.ListAPIView):
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        product_pk = self.request.query_params.get('product_pk', 0)

        if product_pk:
            queryset = Prices.objects.filter(product=product_pk)
        else:
            queryset = Prices.objects.order_by('product', '-date_update')

        return queryset


class PricesAPICreate(generics.CreateAPIView):
    serializer_class = PriceSerializer
    permission_classes = (IsAdminUser,)


class PricesAPIRetrieve(generics.RetrieveAPIView):
    queryset = Prices.objects.all()
    lookup_field = 'product'
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated,)


class PricesAPIUpdate(generics.UpdateAPIView):
    queryset = Prices.objects.all()
    lookup_field = 'product'
    erializer_class = PriceSerializer
    permission_classes = (IsAdminUser,)


class PricesAPIDelete(generics.DestroyAPIView):
    queryset = Prices.objects.all()
    lookup_field = 'product'
    erializer_class = PriceSerializer
    permission_classes = (IsAdminUser,)


class StockProductsAPIList(generics.ListAPIView):
    serializer_class = StockProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        product_pk = self.request.query_params.get('product_pk', 0)
        warehouse_pk = self.request.query_params.get('warehouse_pk', 0)

        if product_pk and warehouse_pk:
            queryset = StockProducts.objects.filter(
                product=product_pk, warehouse=warehouse_pk)
        elif product_pk:
            queryset = StockProducts.objects.filter(product=product_pk)
        elif warehouse_pk:
            queryset = StockProducts.objects.filter(warehouse=warehouse_pk)
        else:
            queryset = StockProducts.objects.order_by('product', 'warehouse')

        return queryset


class StockProductsAPICreate(generics.CreateAPIView):
    serializer_class = StockProductSerializer
    permission_classes = (IsAdminUser,)


class StockProductsAPIRetrieve(generics.RetrieveAPIView):
    queryset = StockProducts.objects.all()
    lookup_field = 'product'
    serializer_class = StockProductSerializer
    permission_classes = (IsAuthenticated,)


class StockProductsAPIUpdate(generics.UpdateAPIView):
    queryset = StockProducts.objects.all()
    lookup_field = 'product'
    serializer_class = StockProductSerializer
    permission_classes = (IsAdminUser,)


class StockProductsAPIDelete(generics.DestroyAPIView):
    queryset = StockProducts.objects.all()
    lookup_field = 'product'
    serializer_class = StockProductSerializer
    permission_classes = (IsAdminUser,)


# Возвращает строки корзины по ID мессенжера, если корзина создана в телеграмме
class CartProductAPILIst(generics.ListAPIView):
    serializer_class = CartProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        id_messenger = self.request.query_params.get('id_messenger', 0)
        # user_pk = self.request.query_params.get('user_pk', 0)
        cart_pk = self.request.query_params.get('cart_pk', 0)
        product_pk = self.request.query_params.get('product_pk', 0)

        if id_messenger and cart_pk and product_pk:
            queryset = CartProduct.objects.filter(
                id_anonymous=id_messenger, cart=cart_pk, product_id=product_pk)
        elif id_messenger and cart_pk:
            queryset = CartProduct.objects.filter(
                id_anonymous=id_messenger, cart=cart_pk)
        elif id_messenger:
            queryset = CartProduct.objects.filter(id_anonymous=id_messenger)
        elif cart_pk:
            queryset = CartProduct.objects.filter(cart=cart_pk)
        else:
            queryset = CartProduct.objects.all()

        return queryset


# Создаю строку товара для корзины (пока отдельно)
class CartProductAPICreate(generics.CreateAPIView):
    serializer_class = CartProductCreateSerializer
    permission_classes = (IsAuthenticated,)


# product - уникальная строка, так как не может один и тот же товар быть в разных строках корзины
class CartProductAPIUpdate(generics.UpdateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = (IsAuthenticated,)


class CartProductAPIDelete(generics.DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = (IsAuthenticated,)


class CartAPICreate(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)


class CartAPIRetrieve(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    lookup_field = 'user'
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)


class CartAPIUpdate(generics.UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)


class CartAPIDelete(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)


class OrdersAPIList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrdersAPICreate(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrderAPIRetrieve(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    lookup_field = 'number'
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)


class OrderAPIUpdate(generics.UpdateAPIView):
    queryset = Cart.objects.all()
    lookup_field = 'number'
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)


class OrderAPIDelete(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    lookup_field = 'number'
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
