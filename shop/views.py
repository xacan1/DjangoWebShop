from django.views.generic import FormView, ListView, DetailView, CreateView
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
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
    model = CartProduct
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # cart_info = services.get_cart_full_info(self.request.user)
        c_def = self.get_user_context(title='Корзина')
        return {**context, **c_def}


class CheckoutView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Оформление заказа', form_login=LoginUserForm)
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


# выводит либо список категорий либо список номенклатуры если в категории больше нет подкатегорий
class CategoryProductListView(DataMixin, FormView):
    form_class = SimpleForm
    slug_url_kwarg = 'category_slug'

    def get_template_names(self) -> list[str]:
        template_names = []

        if hasattr(self, 'price_products') and self.price_products:
            template_names.append('shop/product-list.html')
        else:
            template_names.append('shop/category-grids.html')

        return template_names

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('category_slug', '')
        parent_categories = services.get_parents_category(slug, [])
        self.price_products = services.get_products_prices_for_category(slug)

        if self.price_products:
            total_show_product = 10
            paginator = Paginator(self.price_products, total_show_product)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            c_def = self.get_user_context(title='Список товаров',
                                          total_show_product=total_show_product,
                                          parent_categories=parent_categories,
                                          page_obj=page_obj)
        else:
            category, nested_categories = services.get_nested_categories(slug)
            c_def = self.get_user_context(title='Список категорий',
                                          current_category=category,
                                          nested_categories=nested_categories,
                                          parent_categories=parent_categories)

        return {**context, **c_def}


class SearchView(DataMixin, ListView):
    template_name = 'shop/product-list.html'
    paginate_by = 10

    def get_queryset(self) -> models.QuerySet[Product]:
        q = self.request.GET.get('q')
        queryset = services.search_products(q)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        c_def = self.get_user_context(title=q,
                                      search_text=q,
                                      total_show_product=self.paginate_by)

        return {**context, **c_def}


class ProductDetailView(DataMixin, DetailView):
    model = Product
    template_name = 'shop/product-details.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product_data'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        product_pk = kwargs['object'].pk
        slug = kwargs['object'].category.slug
        images = kwargs['object'].get_images.all()
        stocks = kwargs['object'].get_stock_product.all()

        prices = kwargs['object'].get_prices.all()  # пока нет выбора типов цен
        attributes = services.get_attributes_product(product_pk)
        parent_categories = services.get_parents_category(slug, [])
        c_def = self.get_user_context(title='Карточка товара',
                                      parent_categories=parent_categories,
                                      product_images=images,
                                      product_stocks=stocks,
                                      product_prices=prices,
                                      product_attributes=attributes)
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
