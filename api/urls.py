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
    # path('api/v1/attributes', AttributeAPIList.as_view(), name='attribute-list'),
    # path('api/v1/attributes_create', AttributeAPICreate.as_view(), name='attribute-list'),
    # path('api/v1/attributes/<int:pk>', AttributeAPIRetrieve.as_view()),
    # path('api/v1/attributes_update/<int:pk>', AttributeAPIUpdate.as_view()),
    # path('api/v1/attributes_delete/<int:pk>', AttributeAPIDelete.as_view()),
    # path('api/v1/attributes/values', AttributeValuesAPIList.as_view(), name='attributes-values-list'),
    # path('api/v1/attributes/values_create', AttributeValuesAPICreate.as_view()),
    # path('api/v1/attributes/values/<int:pk>', AttributeValuesAPIRetrieve.as_view()),
    # path('api/v1/attributes/values_update/<int:pk>', AttributeValuesAPIUpdate.as_view()),
    # path('api/v1/attributes/values_delete/<int:pk>', AttributeValuesAPIDelete.as_view()),
    # path('api/v1/products/attribute_values', AttributeProductValuesAPIList.as_view()),
    # path('api/v1/products/attribute_values_create', AttributeProductValuesAPICreate.as_view()),
    # path('api/v1/products/attribute_values/<int:pk>', AttributeProductValuesAPIRetrieve.as_view()),
    # path('api/v1/products/attribute_values_update/<int:pk>', AttributeProductValuesAPIUpdate.as_view()),
    # path('api/v1/products/attribute_values_delete/<int:pk>', AttributeProductValuesAPIDelete.as_view()),
    # path('api/v1/products/categories', CategoryAPIList.as_view()),
    # path('api/v1/products/categories_create', CategoryAPICreate.as_view()),
    # path('api/v1/products/categories/<int:pk>', CategoryAPIRetrieve.as_view()),
    # path('api/v1/products/categories_update/<int:pk>', CategoryAPIUpdate.as_view()),
    # path('api/v1/products/categories_delete/<int:pk>', CategoryAPIDelete.as_view()),
    # path('api/v1/products/favorites', FavoriteProductAPIList.as_view()),
    # path('api/v1/products/favorites_create', FavoriteProductAPICreate.as_view()),
    # path('api/v1/products/favorites/<int:pk>', FavoriteProductAPIRetrieve.as_view()),
    # path('api/v1/products/favorites_update/<int:pk>', FavoriteProductAPIUpdate.as_view()),
    # path('api/v1/products/favorites_delete/<int:pk>', FavoriteProductAPIDelete.as_view()),
    # path('api/v1/products/images', ImageProductAPIList.as_view()),
    # path('api/v1/products/images_create', ImageProductAPICreate.as_view()),
    # path('api/v1/products/images/<int:pk>', ImageProductAPIRetrieve.as_view()),
    # path('api/v1/products/images_update/<int:pk>', ImageProductAPIUpdate.as_view()),
    # path('api/v1/products/images_delete/<int:pk>', ImageProductAPIDelete.as_view()),
    # path('api/v1/products', ProductAPIList.as_view()),
    # path('api/v1/products_create', ProductAPICreate.as_view()),
    # path('api/v1/products/<int:pk>', ProductAPIRetrieve.as_view()),
    # path('api/v1/products_update/<int:pk>', ProductAPIUpdate.as_view()),
    # path('api/v1/products_delete/<int:pk>', ProductAPIDelete.as_view()),
    # path('api/v1/currencies', CurrencyAPIList.as_view()),
    # path('api/v1/currencies_create', CurrencyAPICreate.as_view()),
    # path('api/v1/currencies/<int:pk>', CurrencyAPIRetrieve.as_view()),
    # path('api/v1/currencies_update/<int:pk>', CurrencyAPIUpdate.as_view()),
    # path('api/v1/currencies_delete/<int:pk>', CurrencyAPIDelete.as_view()),
    # path('api/v1/price_types', PriceTypeAPIList.as_view()),
    # path('api/v1/price_types_create', PriceTypeAPICreate.as_view()),
    # path('api/v1/price_types/<int:pk>', PriceTypeAPIRetrieve.as_view()),
    # path('api/v1/price_types_update/<int:pk>', PriceTypeAPIUpdate.as_view()),
    # path('api/v1/price_types_delete/<int:pk>', PriceTypeAPIDelete.as_view()),
    # path('api/v1/prices', PricesAPIList.as_view()),
    # path('api/v1/prices_create', PricesAPICreate.as_view()),
    # path('api/v1/prices/<int:product>', PricesAPIRetrieve.as_view()),
    # path('api/v1/prices_update/<int:product>', PricesAPIUpdate.as_view()),
    # path('api/v1/prices_delete/<int:product>', PricesAPIDelete.as_view()),
    # path('api/v1/stocks', StockProductsAPIList.as_view()),
    # path('api/v1/stocks_create', StockProductsAPICreate.as_view()),
    # path('api/v1/stocks/<int:product>', StockProductsAPIRetrieve.as_view()),
    # path('api/v1/stocks_update/<int:product>', StockProductsAPIUpdate.as_view()),
    # path('api/v1/stocks_delete/<int:product>', StockProductsAPIDelete.as_view()),
    # path('api/v1/warehouses', WarehouseAPIList.as_view()),
    # path('api/v1/warehouses_create', WarehouseAPICreate.as_view()),
    # path('api/v1/warehouses/<int:pk>', WarehouseAPIRetrieve.as_view()),
    # path('api/v1/warehouses_update/<int:pk>', WarehouseAPIUpdate.as_view()),
    # path('api/v1/warehouses_delete/<int:pk>', WarehouseAPIDelete.as_view()),
    # path('api/v1/carts/product_to_cart', CartProductAPILIst.as_view()), # получить список товаров в корзине или заказе по ID мессенджера
    # path('api/v1/carts/product_to_cart_create', CartProductAPICreate.as_view()), # создать строку Корзины или Заказа, но лучше это сделать через update_product_to_cart
    # path('api/v1/carts/product_to_cart_update/<int:pk>', CartProductAPIUpdate.as_view()),
    # path('api/v1/carts/product_to_cart_delete/<int:pk>', CartProductAPIDelete.as_view()),
    # path('api/v1/carts_create', CartAPICreate.as_view()),
    # path('api/v1/carts/<int:user>', CartAPIRetrieve.as_view()),
    # path('api/v1/carts_update/<int:pk>', CartAPIUpdate.as_view()),
    # path('api/v1/carts_delete/<int:pk>', CartAPIDelete.as_view()),
    # path('api/v1/statuses', StatusesAPIList.as_view()),
    # path('api/v1/statuses_create', StatusesAPICreate.as_view()),
    # path('api/v1/statuses/<int:pk>', StatusesAPIRetrieve.as_view()),
    # path('api/v1/statuses_update/<int:pk>', StatusesAPIList.as_view()),
    # path('api/v1/statuses_delete/<int:pk>', StatusesAPIList.as_view()),
    # path('api/v1/payment_types', PaymentTypesAPIList.as_view()),
    # path('api/v1/payment_types_create', PaymentTypesAPICreate.as_view()),
    # path('api/v1/payment_types/<int:pk>', PaymentTypesAPIRetrieve.as_view()),
    # path('api/v1/payment_types_update/<int:pk>', PaymentTypesAPIUpdate.as_view()),
    # path('api/v1/payment_types_delete/<int:pk>', PaymentTypesAPIDelete.as_view()),
    # path('api/v1/delivery_types', DeliveryTypesAPIList.as_view()),
    # path('api/v1/delivery_types_create', DeliveryTypesAPICreate.as_view()),
    # path('api/v1/delivery_types/<int:pk>', DeliveryTypesAPIRetrieve.as_view()),
    # path('api/v1/delivery_types_update/<int:pk>', DeliveryTypesAPIUpdate.as_view()),
    # path('api/v1/delivery_types_delete/<int:pk>', DeliveryTypesAPIDelete.as_view()),
    # path('api/v1/coupons', CouponsAPIList.as_view()),
    # path('api/v1/coupons_create', CouponsAPICreate.as_view()),
    # path('api/v1/coupons/<int:pk>', CouponsAPIRetrieve.as_view()),
    # path('api/v1/coupons_update/<int:pk>', CouponsAPIUpdate.as_view()),
    # path('api/v1/coupons_delete/<int:pk>', CouponsAPIDelete.as_view()),
    # path('api/v1/orders', OrdersAPIList.as_view()),
    # path('api/v1/orders_create', OrdersAPICreate.as_view()),
    # path('api/v1/orders/<str:number>', OrderAPIRetrieve.as_view()),
    # path('api/v1/orders_update/<int:pk>', OrderAPIUpdate.as_view()),
    # path('api/v1/orders_delete/<int:pk>', OrderAPIDelete.as_view()),
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