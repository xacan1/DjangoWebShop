from django.views.generic import FormView, ListView, DetailView, CreateView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from shop.forms import *
from shop import services
from shop.models import *
from shop.mixins import DataMixin


class IndexView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Маркет скидок')
        return {**context, **c_def}


class PageNotFound(FormView):
    form_class = SimpleForm
    template_name = 'shop/page404.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response


class AboutAsView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/about-us.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О нас')
        return {**context, **c_def}


class LoginUserView(DataMixin, auth_views.LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(auth_views.LogoutView):
    next_page = 'home'


class RegisterUserView(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('registration-success')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}


class RegisterUserSuccessView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/registration-success.html'


class CartView(DataMixin, ListView):
    model = Cart
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Корзина')
        return {**context, **c_def}


class CheckoutView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Оформление заказа', form_login=LoginUserForm)
        # c_def = {'title': 'Оформление заказа'}
        return {**context, **c_def}


class ContactView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/contact.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return {**context, **c_def}


class FaqView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/faq.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='FAQ')
        return {**context, **c_def}


class CategoryProductListView(DataMixin, FormView):
    form_class = SimpleForm
    slug_url_kwarg = 'category_slug'

    def get_template_names(self) -> list[str]:
        template_names = []
        slug = self.kwargs.get('category_slug', '')
        products = services.get_products_for_category(slug)

        if products:
            template_names.append('shop/product-list.html')
        else:
            template_names.append('shop/category-grids.html')

        return template_names

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('category_slug', '')
        products = services.get_products_for_category(slug)

        if products:
            c_def = self.get_user_context(
                title='Список товаров', products=products)
        else:
            parents = services.get_parents_category(slug, [])
            slug, name, nested_categories = services.get_nested_categories(slug)
            c_def = self.get_user_context(title='Список категорий',
                                          current_cat_name=name,
                                          nested_categories=nested_categories,
                                          parents=parents)

        return {**context, **c_def}


class ProfileUserView(DataMixin, DetailView):
    model = CustomUser
    template_name = 'shop/index.html'
    context_object_name = 'user_data'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Профиль пользователя')
        return {**context, **c_def}
