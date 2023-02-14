from django.views.generic import FormView, ListView, DetailView, CreateView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from shop.forms import *
from shop import services
from shop.models import *
from shop.mixins import DataMixin
from django.http import HttpResponse


class IndexView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Маркет скидок')
        return {**context, **c_def}


class AboutAsView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/about-us.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О нас')
        return {**context, **c_def}


class CartView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Корзина')
        return {**context, **c_def}


class WishlistView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/wishlist.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        wishlist = services.get_favorite_products_info(self.request.user)
        c_def = self.get_user_context(
            title='Избранные товары', wishlist=wishlist)
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
# products_exist - признак что товары есть в категории, даже если и не найдены из-за фильтров
class CategoryProductListView(DataMixin, FormView):
    slug_url_kwarg = 'category_slug'
    price_products = Product.objects.none()
    products_exist = False

    # проверяет если товары есть, то выберает класс формы для списка товаров иначе класс пустой формы
    def get_form_class(self):
        form_class = super().get_form_class()
        slug = self.kwargs.get('category_slug', '')

        if slug and slug != 'root':
            self.price_products, self.products_exist = services.filter_products_for_category(
                slug, self.request.GET)
            self.price_products = services.sorted_products_for_category(
                self.price_products, self.request.GET)

        form_class = ProductListForm if self.products_exist else SimpleForm
        return form_class

    # передадим данные в форму
    def get_initial(self):
        initial = super().get_initial()
        slug = self.kwargs.get('category_slug', '')
        min_max_price = services.get_min_max_price_category(slug)
        initial = {**initial, **min_max_price}
        initial['get_params'] = self.request.GET
        initial['attribute_groups'] = services.get_attributes_category_with_values(
            slug)
        return initial

    def get_template_names(self) -> list[str]:
        template_names = []

        if self.products_exist:
            template_names.append('shop/product-list.html')
        else:
            template_names.append('shop/category-grids.html')

        return template_names

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('category_slug', '')
        parent_categories = services.get_parents_category(slug, [])

        if slug == 'root':
            root_categories = services.get_root_categories()
            c_def = self.get_user_context(title='Каталог',
                                          nested_categories=root_categories)
        elif self.products_exist:
            paginate_by = 10
            paginator = Paginator(self.price_products, paginate_by)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            amount_product_total = paginator.count
            amount_product_from, amount_product_upto = services.count_product_from_to(
                paginate_by, int(page_number), len(page_obj.object_list))

            # добавляю к адресам пагинации параметры запроса, что бы при переходе на другую страницу
            # GET запрос не только содержал номер страницы, но и в точности повторялся по всем параметрам
            add_for_pagination = ''

            for get_param, value in self.request.GET.items():
                if get_param != 'page':
                    add_for_pagination += f'&{get_param}={value}'

            c_def = self.get_user_context(title='Список товаров',
                                          amount_product_from=amount_product_from,
                                          amount_product_upto=amount_product_upto,
                                          amount_product_total=amount_product_total,
                                          parent_categories=parent_categories,
                                          add_for_pagination=add_for_pagination,
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
    min_max_price = {'price__min': 0, 'price__max': 0}
    amount_product_from = 0
    amount_product_upto = 0
    amount_product_total = 0

    # def get_paginate_by(self, queryset: _BaseQuerySet[Any]) -> Optional[int]:
    #     return super().get_paginate_by(queryset)

    def paginate_queryset(self, queryset, page_size) -> tuple[Paginator, int, models.QuerySet[Product], bool]:
        paginator, page, page_obj, has_other_pages = super().paginate_queryset(queryset, page_size)
        self.amount_product_total = paginator.count
        self.amount_product_from, self.amount_product_upto = services.count_product_from_to(
                self.paginate_by, page.number, page_obj.count())
        return paginator, page, page_obj, has_other_pages

    def get_queryset(self) -> models.QuerySet[Product]:
        q = self.request.GET.get('q')
        queryset, self.min_max_price = services.search_products(q)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        add_for_pagination = f'&q={q}'

        c_def = self.get_user_context(title=f'поиск: {q}',
                                      search_text=q,
                                      amount_product_from=self.amount_product_from,
                                      amount_product_upto=self.amount_product_upto,
                                      amount_product_total=self.amount_product_total,
                                      add_for_pagination=add_for_pagination,
                                      min_max_price=self.min_max_price,
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


class AddOrderView(DataMixin, CreateView):
    model = Order
    form_class = AddOrderForm
    template_name = 'shop/checkout.html'
    success_url = reverse_lazy('new-order-success')

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user if self.request.user.is_authenticated else None
        response = super().form_valid(form)
        order = form.instance
        services.changing_cart_rows_to_order_rows(self.request.user, order,
                                                  self.request.session.session_key)
        return response

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        cart = services.get_cart_full_info(user=self.request.user,
                                           session_key=self.request.session.session_key)

        # установим значения формы если пользователь уже залогинен
        if self.request.user.is_authenticated:
            form = self.form_class(initial={'first_name': self.request.user.first_name,
                                            'last_name': self.request.user.last_name,
                                            'email': self.request.user.email,
                                            'phone': self.request.user.phone})
            context['form'] = form

        c_def = self.get_user_context(title='Оформление заказа', cart=cart)
        return {**context, **c_def}


class AddOrderSuccessView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/new-order-success.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Заказ оформлен')
        return {**context, **c_def}


class OrderView(DataMixin, DetailView):
    model = Order
    template_name = 'shop/order.html'
    context_object_name = 'order'
    pk_url_kwarg = 'number'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        order = kwargs['object']
        c_def = self.get_user_context(title=f'{order}')
        return {**context, **c_def}


class OrderCancelConfirmView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/order-cancel-confirm.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        order_pk = self.kwargs.get('number', 0)
        c_def = self.get_user_context(title='Отмена заказа', order_pk=order_pk)
        return {**context, **c_def}


class OrderCancelCompleteView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/order-cancel-complete.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Заказ отменен')
        return {**context, **c_def}
