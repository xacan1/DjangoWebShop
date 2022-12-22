from django.urls import path
from personal_account.views import *


urlpatterns = [
    path('personal-account/', PersonalAccountView.as_view(), name='personal-account'),
    path('personal-account/user-settings/', UserSettingsView.as_view(), name='user-settings'),
    path('personal-account/user-orders/', UserOrdersView.as_view(), name='user-orders'),
    path('personal-account/user-companies/', UserCompaniesView.as_view(), name='user-companies'),
]
