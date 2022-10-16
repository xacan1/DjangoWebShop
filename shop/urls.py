from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('about-us/', AboutAsView.as_view(), name='about-us'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path('cart/', CartView.as_view(), name='cart'),
]
