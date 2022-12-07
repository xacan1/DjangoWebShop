from django.urls import path
from main.views import *

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path('registration-success/', RegisterUserSuccessView.as_view(), name='registration-success'),
    path('profile/<int:user_id>', ProfileUserView.as_view(), name='profile'),
]
