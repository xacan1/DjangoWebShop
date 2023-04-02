from rest_framework.permissions import *


class IsAdminOrReadOnly(BasePermission):
    """
    The request is admin as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsAdminOrIsAuthenticated(BasePermission):
    """
    The request is admin as a user, or is authenticated for read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS and
             request.user and
             request.user.is_authenticated) or
            (request.user and
             request.user.is_staff)
        )

"""
l = [
    < URLPattern '^attributes/values/$' [name = 'AttributeValues-list'] > ,
      < URLPattern '^attributes/values/(?P<pk>[^/.]+)/$' [name = 'AttributeValues-detail'] > ,
        < URLPattern '^attributes/$' [name = 'attribute-list'] > ,
          < URLPattern '^attributes/(?P<pk>[^/.]+)/$' [name = 'attribute-detail'] > , 
          < URLPattern '^products/attributes/values/$' [name = 'AttributeProductValues-list'] > ,
            < URLPattern '^products/attributes/values/(?P<pk>[^/.]+)/$' [name = 'AttributeProductValues-detail'] > ,
              < URLPattern '^products/categories/$' [name = 'Category-list'] > ,
                < URLPattern '^products/categories/(?P<pk>[^/.]+)/$' [name = 'Category-detail'] > , 
                < URLPattern '^products/favorites/$' [name = 'FavoriteProduct-list'] > ,
                  < URLPattern '^products/favorites/(?P<pk>[^/.]+)/$' [name = 'FavoriteProduct-detail'] > ,
                    < URLPattern '^products/images/$' [name = 'ImageProduct-list'] > ,
                      < URLPattern '^products/images/(?P<pk>[^/.]+)/$' [name = 'ImageProduct-detail'] > ,
                        < URLPattern '^products/$' [name = 'Product-list'] > ,
                          < URLPattern '^products/(?P<pk>[^/.]+)/$' [name = 'Product-detail'] > ,
                            < URLPattern '^currencies/$' [name = 'Currency-list'] > ,
                              < URLPattern '^currencies/(?P<pk>[^/.]+)/$' [name = 'Currency-detail'] > , 
                              < URLPattern '^price_types/$' [name = 'PriceType-list'] > ,
                                < URLPattern '^price_types/(?P<pk>[^/.]+)/$' [name = 'PriceType-detail'] > ,
                                  < URLPattern '^prices/$' [name = 'Prices-list'] > , 
                                  < URLPattern '^prices/(?P<pk>[^/.]+)/$' [name = 'Prices-detail'] > , 
                                  < URLPattern '^stocks/$' [name = 'StockProducts-list'] > , 
                                  < URLPattern '^stocks/(?P<pk>[^/.]+)/$' [name = 'StockProducts-detail'] > , 
                                  < URLPattern '^warehouses/$' [name = 'Warehouse-list'] > , 
                                  < URLPattern '^warehouses/(?P<pk>[^/.]+)/$' [name = 'Warehouse-detail'] > , 
                                  < URLPattern '^carts/products/$' [name = 'CartProduct-list'] > , 
                                  < URLPattern '^carts/products/(?P<pk>[^/.]+)/$' [name = 'CartProduct-detail'] > , 
                                  < URLPattern '^carts/$' [name = 'cart-list'] > , 
                                  < URLPattern '^carts/(?P<pk>[^/.]+)/$' [name = 'cart-detail'] > , 
                                  < URLPattern '^statuses/$' [name = 'Status-list'] > , 
                                  < URLPattern '^statuses/(?P<pk>[^/.]+)/$' [name = 'Status-detail'] > , 
                                  < URLPattern '^payment_types/$' [name = 'PaymentType-list'] > , 
                                  < URLPattern '^payment_types/(?P<pk>[^/.]+)/$' [name = 'PaymentType-detail'] > , 
                                  < URLPattern '^delivery_types/$' [name = 'DeliveryType-list'] > , 
                                  < URLPattern '^delivery_types/(?P<pk>[^/.]+)/$' [name = 'DeliveryType-detail'] > , 
                                  < URLPattern '^coupons/$' [name = 'Coupon-list'] > , 
                                  < URLPattern '^coupons/(?P<pk>[^/.]+)/$' [name = 'Coupon-detail'] > , 
                                  < URLPattern '^orders/$' [name = 'Order-list'] > ,
                                    < URLPattern '^orders/(?P<pk>[^/.]+)/$' [name = 'Order-detail']
    ]
"""