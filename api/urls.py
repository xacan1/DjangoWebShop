from django.urls import path, include
from rest_framework import routers
from api.views import *


router = routers.SimpleRouter()
router.register(r'attributes/values', AttributeValuesAPIViewSet, basename='AttributeValues')
router.register(r'attributes', AttributeAPIViewSet)
router.register(r'products/attributes/values', AttributeProductValuesAPIViewSet, basename='AttributeProductValues')
router.register(r'products/categories', CategoryAPIViewSet, basename='Category')
router.register(r'products/favorites', FavoriteProductAPIViewSet, basename='FavoriteProduct')
router.register(r'products/images', ImageProductAPViewSet, basename='ImageProduct')
router.register(r'products', ProductAPIViewSet, basename='Product')
router.register(r'currencies', CurrencyAPIViewSet, basename='Currency')
router.register(r'price_types', PriceTypeAPIViewSet, basename='PriceType')
router.register(r'prices', PricesAPIViewSet, basename='Prices')
router.register(r'stocks', StockProductsAPIViewSet, basename='StockProducts')
router.register(r'warehouses', WarehouseAPIViewSet, basename='Warehouse')
router.register(r'carts/products', CartProductAPIViewSet, basename='CartProduct')
router.register(r'carts', CartAPIViewSet)
router.register(r'statuses', StatusesAPIViewSet, basename='Status')
router.register(r'payment_types', PaymentTypesAPIViewSet, basename='PaymentType')
router.register(r'delivery_types', DeliveryTypesAPIViewSet, basename='DeliveryType')
router.register(r'coupons', CouponsAPIViewSet, basename='Coupon')
router.register(r'orders', OrdersAPIViewSet, basename='Order')

urlpatterns = [
    # REST API общий
    path('api/v1/tokens', TokensAPIList.as_view()),
    path('api/v1/users/<str:email>', UsersAPIRetrieve.as_view()),
    path('api/v1/', include(router.urls)),
    # API специализированный для магазина
    path('api/v1/update_product_to_cart', APIUpdateProductToCart.as_view()),
    path('api/v1/delete_product_from_cart', APIDeleteProductFromCart.as_view()),
    path('api/v1/create_update_order', APICreateUpdateOrder.as_view()), # использует только телеграм бот
    path('api/v1/cancel_order', APICancelOrder.as_view()),
    path('api/v1/check_stock_for_order', APICheckStockForOrder.as_view()),
    path('api/v1/get_cart_info', APIGetCartInfo.as_view()),
    path('api/v1/get_order_info', APIGetOrderInfo.as_view()),
    path('api/v1/get_favorite_products_info', APIGetFavoriteProductsInfo.as_view()),
    path('api/v1/add_favorite_product', APIAddFavoriteProduct.as_view()),
]