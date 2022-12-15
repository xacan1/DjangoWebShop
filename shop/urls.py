from django.urls import path
from shop.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('about-us/', AboutAsView.as_view(), name='about-us'),
    path('cart/', CartView.as_view(), name='cart'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('productlist/<slug:category_slug>', CategoryProductListView.as_view(), name='productlist'),
    path('search/', SearchView.as_view(), name='search'),
    path('productdetails/<slug:product_slug>', ProductDetailView.as_view(), name='productdetails'),
    path('checkout/', AddOrderView.as_view(), name='checkout'),
    path('new-order-success/', AddOrderSuccessView.as_view(), name='new-order-success'),
    path('order/', OrderView.as_view(), name='order'),
]
