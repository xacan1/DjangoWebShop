from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('about-us/', AboutAsView.as_view(), name='about-us'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path('registration-success/', RegisterUserSuccessView.as_view(), name='registration-success'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('profile/<int:user_id>', ProfileUserView.as_view(), name='profile'),
    path('productlist/<slug:category_slug>', CategoryProductListView.as_view(), name='productlist'),
]
