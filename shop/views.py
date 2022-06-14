from django.views.generic import ListView
from rest_framework import generics
from rest_framework.views import Response, Request, APIView 
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *
from . import services


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


# top_level_only - GET-параметр, сообщающий, что нужно вернуть только верхний уровень иерархии групп номенклатуры
# category_pk - если надо вернуть состав только одной группы номенклатуры
# может быть уставнолен только один параметр либо ни одного
class CategoryAPIList(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        top_level_only = self.request.query_params.get('top_level_only', False)
        category_pk = self.request.query_params.get('category_pk', 0)

        if top_level_only:
            queryset = Category.objects.filter(parent=None)
        elif category_pk:
            queryset = Category.objects.filter(parent=category_pk)
        else:
            queryset = Category.objects.all()

        return queryset


class CategoryAPICreate(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class CategoryAPIRetrieve(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class CategoryAPIUpdate(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class CategoryAPIDelete(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class FavoriteProductAPIList(generics.ListAPIView):
    serializer_class = FavoriteProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = FavoriteProduct.objects.filter(**get_params)
        return queryset


class FavoriteProductAPICreate(generics.CreateAPIView):
    serializer_class = FavoriteProductCreateSerializer
    permission_classes = (IsAuthenticated,)


class FavoriteProductAPIRetrieve(generics.RetrieveAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = (IsAuthenticated,)


class FavoriteProductAPIUpdate(generics.UpdateAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductCreateSerializer
    permission_classes = (IsAuthenticated,)


class FavoriteProductAPIDelete(generics.DestroyAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductCreateSerializer
    permission_classes = (IsAuthenticated,)


# Выводит список товаров с остатками по складам и ценами
# category_pk - категория товара (каталог)
# warehouse_pk - склад
class ProductAPIList(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # self.request.data - данные POST запроса
        # self.request.query_params - данные GET запроса
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        category_pk = get_params.get('category_pk', 0)
        warehouse_pk = get_params.get('warehouse_pk', 0)

        if category_pk and warehouse_pk:
            queryset = Product.objects.filter(
                category=category_pk, get_stock_product__warehouse=warehouse_pk)
        elif category_pk:
            queryset = Product.objects.filter(category=category_pk)
        elif warehouse_pk:
            queryset = Product.objects.filter(
                get_stock_product__warehouse=warehouse_pk)
        else:
            queryset = Product.objects.filter(**get_params)

        return queryset


class ProductAPICreate(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)


class ProductAPIRetrieve(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ProductAPIUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)


class ProductAPIDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)


class CurrencyAPIList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAuthenticated,)


class CurrencyAPICreate(generics.CreateAPIView):
    serializer_class = CurrencySerializer
    permission_classes = (IsAdminUser,)


class CurrencyAPIRetrieve(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAuthenticated,)


class CurrencyAPIUpdate(generics.UpdateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAdminUser,)


class CurrencyAPIDelete(generics.DestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAdminUser,)


class PriceTypeAPIList(generics.ListAPIView):
    queryset = PriceType.objects.all()
    serializer_class = PriceTypeSerializer
    permission_classes = (IsAuthenticated,)


class PriceTypeAPIRetrieve(generics.RetrieveAPIView):
    queryset = PriceType.objects.all()
    serializer_class = PriceTypeSerializer
    permission_classes = (IsAuthenticated,)


class PriceTypeAPICreate(generics.CreateAPIView):
    serializer_class = PriceTypeSerializer
    permission_classes = (IsAdminUser,)


class PriceTypeAPIUpdate(generics.UpdateAPIView):
    queryset = PriceType.objects.all()
    serializer_class = PriceTypeSerializer
    permission_classes = (IsAdminUser,)


class PriceTypeAPIDelete(generics.DestroyAPIView):
    queryset = PriceType.objects.all()
    serializer_class = PriceTypeSerializer
    permission_classes = (IsAdminUser,)


class WarehouseAPIList(generics.ListAPIView):
    serializer_class = WarehouseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = Warehouse.objects.filter(**get_params)
        return queryset


class WarehouseAPICreate(generics.CreateAPIView):
    serializer_class = WarehouseSerializer
    permission_classes = (IsAdminUser,)


class WarehouseAPIRetrieve(generics.RetrieveAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = (IsAuthenticated,)


class WarehouseAPIUpdate(generics.UpdateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = (IsAdminUser,)


class WarehouseAPIDelete(generics.DestroyAPIView):
    queryset = Warehouse.objects.all()
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
            queryset = Prices.objects.order_by('product')

        return queryset


class PricesAPICreate(generics.CreateAPIView):
    serializer_class = PriceCreateSerializer
    permission_classes = (IsAdminUser,)


class PricesAPIRetrieve(generics.RetrieveAPIView):
    queryset = Prices.objects.all()
    lookup_field = 'product'
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated,)


class PricesAPIUpdate(generics.UpdateAPIView):
    queryset = Prices.objects.all()
    lookup_field = 'product'
    serializer_class = PriceCreateSerializer
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
        params = {}

        if product_pk:
            params['product'] = product_pk

        if warehouse_pk:
            params['warehouse'] = warehouse_pk

        if params:
            queryset = StockProducts.objects.filter(**params)
        else:
            queryset = StockProducts.objects.order_by('product', 'warehouse')

        return queryset


class StockProductsAPICreate(generics.CreateAPIView):
    serializer_class = StockProductCreateSerializer
    permission_classes = (IsAdminUser,)


class StockProductsAPIRetrieve(generics.RetrieveAPIView):
    queryset = StockProducts.objects.all()
    lookup_field = 'product'
    serializer_class = StockProductSerializer
    permission_classes = (IsAuthenticated,)


class StockProductsAPIUpdate(generics.UpdateAPIView):
    queryset = StockProducts.objects.all()
    lookup_field = 'product'
    serializer_class = StockProductCreateSerializer
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
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        # queryset = CartProduct.objects.filter(**get_params).annotate(quantity_sum=models.Sum('quantity')).order_by()
        queryset = CartProduct.objects.filter(**get_params)
        return queryset


# Создаю строку товара для корзины (отдельным сериализатором)
class CartProductAPICreate(generics.CreateAPIView):
    serializer_class = CartProductCreateSerializer
    permission_classes = (IsAuthenticated,)


# product - уникальная строка, так как не может один и тот же товар быть в разных строках корзины
class CartProductAPIUpdate(generics.UpdateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductCreateSerializer
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


class StatusesAPIList(generics.ListAPIView):
    serializer_class = StatusSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = Status.objects.filter(**get_params)
        return queryset


class PaymentTypesAPIList(generics.ListAPIView):
    serializer_class = PaymentTypeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = PaymentType.objects.filter(**get_params)
        return queryset


class DeliveryTypesAPIList(generics.ListAPIView):
    serializer_class = DeliveryTypeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = DeliveryType.objects.filter(**get_params)
        return queryset


class OrdersAPIList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        
        user_pk = self.request.user.pk
        id_messenger = get_params.get('id_messenger', 0)
        paid = get_params.get('paid', False)

        if user_pk and id_messenger:
            queryset = services.get_orders_for_user(user_pk, id_messenger, paid)
        else:
            queryset = Order.objects.filter(**get_params)
 
        return queryset


class OrdersAPICreate(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)


class OrderAPIRetrieve(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    lookup_field = 'number'
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrderAPIUpdate(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)


class OrderAPIDelete(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


# API специализированный для магазина


class APIUpdateProductToCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        data_response = services.add_delete_update_product_to_cart(request.user, request.data)
        return Response(data_response)


class APIDeleteProductFromCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        data_response = services.delete_product_from_cart_or_order(request.user, request.data)
        return Response(data_response)


class APICreateUpdateOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        data_response = services.create_or_update_order(request.user, request.data)
        return Response(data_response)


class APICheckStockForOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        get_params = request.query_params
        get_params = {param: get_params[param] for param in get_params}
        order_pk = int(get_params.get('order_pk', 0))
        result = services.check_stock_in_order(order_pk)
        return Response(result)


class APIGetOrderInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        get_params = request.query_params
        get_params = {param: get_params[param] for param in get_params}
        order_info = services.get_order_full_info(request.user, get_params)
        return Response(order_info)


class APIGetCartInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        get_params = request.query_params
        get_params = {param: get_params[param] for param in get_params}
        cart_info = services.get_cart_full_info(request.user, get_params)
        return Response(cart_info)
