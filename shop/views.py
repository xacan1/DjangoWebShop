from django.views.generic import FormView, ListView, DetailView, CreateView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import *
from .models import *


class IndexView(ListView):
    model = Product
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title='Маркет скидок', form_login=LoginUserForm)
        c_def = {'title': 'Маркет скидок'}
        return {**context, **c_def}


class PageNotFound(FormView):
    form_class = SimpleForm
    template_name = 'shop/page404.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response


class AboutAsView(FormView):
    form_class = SimpleForm
    template_name = 'shop/about-us.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'О нас'}
        return {**context, **c_def}


class LoginUserView(auth_views.LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(
        #     title='Авторизация', form_login=LoginUserForm)
        c_def = {'title': 'Авторизация', 'form_login': LoginUserForm}
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(auth_views.LogoutView):
    next_page = 'home'


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('registration_successful')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(
        #     title='Регистрация', form_login=LoginUserForm)
        c_def = {'title': 'Регистрация', 'form_login': LoginUserForm}

        return {**context, **c_def}


class CartView(ListView):
    model = Cart
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title='Корзина', form_login=LoginUserForm)
        c_def = {'title': 'Корзина'}
        return {**context, **c_def}


class CheckoutView(FormView):
    form_class = SimpleForm
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title='Корзина', form_login=LoginUserForm)
        c_def = {'title': 'Оформление заказа'}
        return {**context, **c_def}


class ContactView(FormView):
    form_class = SimpleForm
    template_name = 'shop/contact.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title='Корзина', form_login=LoginUserForm)
        c_def = {'title': 'Форма связи'}
        return {**context, **c_def}


class FaqView(FormView):
    form_class = SimpleForm
    template_name = 'shop/faq.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title='Корзина', form_login=LoginUserForm)
        c_def = {'title': 'FAQ'}
        return {**context, **c_def}
