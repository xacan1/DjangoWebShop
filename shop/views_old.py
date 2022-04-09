from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *


class IndexView(ListView):
    model = Category
    template_name = 'shop/index.html'


class GenericCRUD(generics.mixins.CreateModelMixin,
                  generics.mixins.RetrieveModelMixin,
                  generics.mixins.UpdateModelMixin,
                  generics.mixins.DestroyModelMixin,
                  generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryAPIList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class CategoryAPIDetail(GenericCRUD):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        method = self.request.query_params.get('method', 0)
        external_code = self.request.query_params.get('external_code', 0)

        if external_code and method == 'get' and self.request.method == 'GET':
            obj = get_object_or_404(queryset, external_code=external_code)
        elif external_code and method == 'update' and (self.request.method == 'PUT' or self.request.method == 'PATCH'):
            obj = get_object_or_404(queryset, external_code=external_code)
        else:
            raise Http404('Метод не известен')

        return obj

    def get_queryset(self):
        external_code = self.request.query_params.get('external_code', 0)

        if external_code:
            queryset = Category.objects.filter(external_code=external_code)
        else:
            queryset = Category.objects.all()

        return queryset


class CategoryAPICreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    lookup_field = 'external_code'
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


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
# category - категория товара (каталог)
class ProductAPIList(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # self.request.data - данные POST запроса
        # self.request.query_params - данные GET запроса
        category = self.request.query_params.get('category', 0)

        if category:
            queryset = Product.objects.filter(category=category)
        else:
            queryset = Product.objects.all()

        return queryset


class WarehouseAPIList(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = (IsAuthenticated,)


class PriceAPIList(generics.ListAPIView):
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        product_pk = self.request.query_params.get('product_pk', 0)

        if product_pk:
            queryset = Prices.objects.filter(product=product_pk)
        else:
            queryset = Prices.objects.all()

        return queryset


# Просмотр карточки товара
class ProductAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


# Тут возможно при создании надо пользоватья общим классом,
# так как нужно работать с двумя моделями: сначала создать корзину(пустую), затем создавать строки и добвлять их в корзину


class AddProductToCart(generics.CreateAPIView):
    serializer_class = CartProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset()


class UpdateProductInCart(generics.UpdateAPIView):
    pass


class DeleteProductFromCart(generics.DestroyAPIView):
    pass
