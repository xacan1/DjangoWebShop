from django.db.models.signals import post_save, post_delete
from .models import *
from .services import get_default_status


# после записи или удаления CartProduct пересчитаем Cart
def update_cart_product_signal(sender, **kwars) -> None:
    cart_order_product = kwars['instance']
    cart_user = cart_order_product.user.get_user_cart

    if cart_user:
        cart_pk = cart_user.pk
    else:
        return

    # в любом случае пересчитаю Корзину
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

    # если есть Заказ, то пересчитаю его и сменю статус
    if cart_order_product.order:
        order_pk = cart_order_product.order.pk

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
