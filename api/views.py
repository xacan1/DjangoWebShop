from rest_framework import generics, viewsets
from rest_framework.views import Response, Request, APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from api.permissions import IsAdminOrIsAuthenticated
from shop.models import *
from api.serializers import *
from shop import services


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
class CategoryAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

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


class FavoriteProductAPIViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = FavoriteProduct.objects.filter(**get_params)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = FavoriteProductSerializer
        else:
            serializer_class = FavoriteProductCreateSerializer

        return serializer_class


# Выводит список товаров с остатками по складам и ценами
# category_pk - категория товара (каталог)
# warehouse_pk - склад
class ProductAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

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


class ImageProductAPViewSet(viewsets.ModelViewSet):
    serializer_class = ImageProductSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = ImageProduct.objects.filter(**get_params)
        return queryset


class AttributeAPIViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)


class AttributeValuesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = AttributeValuesSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = AttributeValues.objects.filter(**get_params)
        return queryset


class AttributeProductValuesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = AttributeProductValuesSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = AttributeProductValues.objects.filter(**get_params)
        return queryset


class CurrencyAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CurrencySerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = Currency.objects.filter(**get_params)
        return queryset


class PriceTypeAPIViewSet(viewsets.ModelViewSet):
    serializer_class = PriceTypeSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = PriceType.objects.filter(**get_params)
        return queryset


class WarehouseAPIViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = Warehouse.objects.filter(**get_params)
        return queryset


class PricesAPIViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}

        if get_params:
            queryset = Prices.objects.filter(**get_params)
        else:
            queryset = Prices.objects.order_by('product')

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = PriceSerializer
        else:
            serializer_class = PriceCreateSerializer

        return serializer_class


class StockProductsAPIViewSet(viewsets.ModelViewSet):
    serializer_class = StockProductSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}

        if get_params:
            queryset = StockProducts.objects.filter(**get_params)
        else:
            queryset = StockProducts.objects.order_by('product', 'warehouse')

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = StockProductSerializer
        else:
            serializer_class = StockProductCreateSerializer

        return serializer_class


# Возвращает строки корзины по ID мессенжера, если корзина создана в телеграмме
class CartProductAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CartProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = CartProduct.objects.filter(**get_params)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = CartProductSerializer
        else:
            serializer_class = CartProductCreateSerializer

        return serializer_class


class CartAPIViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)


class StatusesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = Status.objects.filter(**get_params)
        return queryset


class PaymentTypesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentTypeSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = PaymentType.objects.filter(**get_params)
        return queryset


class DeliveryTypesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryTypeSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = DeliveryType.objects.filter(**get_params)
        return queryset


class CouponsAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    permission_classes = (IsAdminOrIsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}
        queryset = Coupon.objects.filter(**get_params)
        return queryset


class OrdersAPIViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        get_params = self.request.query_params
        get_params = {param: get_params[param] for param in get_params}

        user_pk = self.request.user.pk
        id_messenger = get_params.get('id_messenger', 0)
        paid = get_params.get('paid', False)

        if user_pk and id_messenger:
            queryset = services.get_orders_for_user(
                user_pk, id_messenger, paid)
        else:
            queryset = Order.objects.filter(**get_params)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = OrderSerializer
        else:
            serializer_class = OrderCreateSerializer

        return serializer_class


# API специализированный для магазина


class APIUpdateProductToCart(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        data_response = services.add_delete_update_product_to_cart(
            request.user, request.data, self.request.session.session_key)
        return Response(data_response)


class APIDeleteProductFromCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        data_response = services.delete_product_from_cart_or_order(
            request.user, request.data)
        return Response(data_response)


class APICreateUpdateOrder(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        data_response = services.create_or_update_order_for_messenger(
            request.user, request.data)
        return Response(data_response)


class APICheckStockForOrder(APIView):
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        get_params = request.query_params
        get_params = {param: get_params[param] for param in get_params}
        session_key = '' if self.request.session.session_key is None else self.request.session.session_key
        old_session_key = self.request.session.get('sessionid', '')

        # сессия изменилась из-за логина, надо сделать слияние анонимной корзины с пользовательской
        if session_key != old_session_key and request.user.is_authenticated:
            services.merging_two_shopping_carts(request.user, old_session_key)

        cart_info = services.get_cart_full_info(
            request.user, get_params=get_params, session_key=session_key)
        return Response(cart_info)


class APIGetFavoriteProductsInfo(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request: Request) -> Response:
        wishlist_info = services.get_favorite_products_info(request.user)
        return Response(wishlist_info)


class APIAddFavoriteProduct(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        data_response = services.add_favorite_product(
            request.user, request.data)
        return Response(data_response)
