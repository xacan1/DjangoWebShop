from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from .services import *


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
def update_cart_product_signal(sender, **kwargs) -> None:
    product_row = kwargs['instance']

    try:
        cart = product_row.cart
    except ObjectDoesNotExist:
        return

    # try:
    #     order = product_row.order
    # except ObjectDoesNotExist:
    #     return

    if cart:
        cart_pk = product_row.cart.pk

        # в любом случае пересчитаю общие суммы Корзины
        cart_sum = CartProduct.objects.filter(cart=cart_pk, order=None).aggregate(
            sum_quantity=models.Sum('quantity'),
            sum_amount=models.Sum('amount'),
            sum_discount=models.Sum('discount')
        )

        queryset = Cart.objects.filter(pk=cart_pk)

        if queryset.exists():
            cart = queryset[0]
            cart.quantity = cart_sum['sum_quantity'] if cart_sum['sum_quantity'] else 0
            cart.amount = cart_sum['sum_amount'] if cart_sum['sum_amount'] else 0
            cart.discount = cart_sum['sum_discount'] if cart_sum['sum_discount'] else 0
            cart.save()

    # если есть Заказ, то пересчитаю его общие суммы и сменю статус
    if product_row.order:
        order_pk = product_row.order.pk

        order_sum = CartProduct.objects.filter(order=order_pk, cart=None).aggregate(
            sum_quantity=models.Sum('quantity'),
            sum_amount=models.Sum('amount'),
            sum_discount=models.Sum('discount')
        )

        queryset = Order.objects.filter(pk=order_pk)

        if queryset.exists():
            order = queryset[0]
            order.quantity = order_sum['sum_quantity'] if order_sum['sum_quantity'] else 0
            order.amount = order_sum['sum_amount'] if order_sum['sum_amount'] else 0
            order.discount = order_sum['sum_discount'] if order_sum['sum_discount'] else 0
            order.status_id = 5 if order.quantity == 0 or order.amount == 0 else get_default_status()
            order.save()
