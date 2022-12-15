from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from shop.models import *
from shop import services


def set_default_photo_product(sender, **kwargs) -> None:
    photo_product = kwargs['instance']

    if photo_product.default:
        product = Product.objects.get(pk=photo_product.product.pk)
        product.photo = photo_product.photo
        product.save()


def set_default_currency(sender, **kwargs) -> None:
    queryset = Currency.objects.filter(default=True)
    currency = kwargs['instance']

    if not queryset.exists() or (queryset.count() == 1 and queryset.first().digital_code == currency.digital_code):
        currency.default = True


def set_default_price_type(sender, **kwargs) -> None:
    queryset = PriceType.objects.filter(default=True)
    price_type = kwargs['instance']

    if not queryset.exists() or (queryset.count() == 1 and queryset.first().external_code == price_type.external_code):
        price_type.default = True


# стандартно расчитывает суммы в строке Корзины или Заказа, данные строки передаются в виде словаря
# ВНИМАНИЕ! Цена не проверяется, может быть хоть нулевой
def calculate_product_cart_table_row(sender, **kwargs) -> None:
    product_row = kwargs['instance']

    if product_row.quantity < 0:
        product_row.quantity = 0

    amount_without_discount = product_row.price * product_row.quantity
    discount = amount_without_discount * product_row.discount_percentage / 100
    product_row.discount = discount
    product_row.amount = amount_without_discount - discount


# после записи или удаления CartProduct пересчитаем Cart
def update_cart_product(sender, **kwargs) -> None:
    product_row = kwargs['instance']

    try:
        # пересчитаю общие суммы Корзины
        if product_row.cart:
            cart_pk = product_row.cart.pk
            services.update_cart_sum(cart_pk)

    except ObjectDoesNotExist:
        pass

    try:
        if product_row.order:
            order_pk = product_row.order.pk
            services.update_order_sum(order_pk)

    except ObjectDoesNotExist:
        pass


def set_default_status_and_currency_order(sender, **kwargs) -> None:
    order = kwargs['instance']

    try:
        status = order.status
    except ObjectDoesNotExist:
        order.status = services.get_default_status()

    try:
        currency = order.currency
    except ObjectDoesNotExist:
        order.currency = services.get_default_currency()
