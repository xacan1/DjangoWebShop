from django.db.models.signals import pre_save, post_save, post_delete
from .services import *


def set_default_currency(sender, **kwars) -> None:
    queryset = Currency.objects.filter(default=True)

    if not queryset.exists():
        currency = kwars['instance']
        currency.default = True


def set_default_price_type(sender, **kwars) -> None:
    queryset = PriceType.objects.filter(default=True)

    if not queryset.exists():
        price_type = kwars['instance']
        price_type.default = True


# стандартно расчитывает суммы в строке Корзины или Заказа, данные строки передаются в виде словаря
# ВНИМАНИЕ! Цена не проверяется, может быть хоть нулевой
def calculate_product_cart_table_row(sender, **kwars) -> None:
    product_row = kwars['instance']

    if product_row.quantity < 0:
        product_row.quantity = 0

    amount_without_discount = product_row.price * product_row.quantity
    discount = amount_without_discount * product_row.discount_percentage / 100
    product_row.discount = discount
    product_row.amount = amount_without_discount - discount


# после записи или удаления CartProduct пересчитаем Cart
def update_cart_product_signal(sender, **kwars) -> None:
    product_row = kwars['instance']
    cart_user = product_row.user.get_user_cart

    if cart_user:
        cart_pk = cart_user.pk
    else:
        return

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
