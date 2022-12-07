from django.views.generic import FormView, ListView, DetailView, CreateView
from django.core.paginator import Paginator
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


class CheckoutView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оформление заказа')
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

