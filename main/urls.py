from django.urls import path, re_path
from main.views import *


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('registration/', RegisterUserView.as_view(), name='registration'),
    path('registration-success/', RegisterUserSuccessView.as_view(), name='registration-success'),
    re_path(r'^passwords/change/$', VersaPasswordChangeView.as_view(), name='password_change'),
    re_path(r'^passwords/change/done/$', VersaPasswordChangeDoneView.as_view(), name='password_change_done'),
    re_path(r'^passwords/reset/$', VersaPasswordResetView.as_view(), name='password_reset'),
    re_path(r'^passwords/reset/done/$', VersaPasswordResetDoneView.as_view(),  name='password_reset_done'),
    re_path(r'^passwords/reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', VersaPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^passwords/reset/complete/$', VersaPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
