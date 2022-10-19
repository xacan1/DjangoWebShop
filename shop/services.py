from decimal import Decimal
from .serializers import *
from .models import *


def get_default_status() -> int:
    status_pk = 0
    queryset = Status.objects.filter(for_bot=True)

    if queryset.exists():
        status_pk = queryset[0].pk

    return status_pk


def get_default_delivery_type() -> int:
    delivery_type_pk = 0
    queryset = DeliveryType.objects.filter(for_bot=True)

    if queryset.exists():
        delivery_type_pk = queryset[0].pk

    return delivery_type_pk


def get_default_payment_type() -> int:
    payment_type_pk = 0
    queryset = PaymentType.objects.filter(for_bot=True)

    if queryset.exists():
        payment_type_pk = queryset[0].pk

    return payment_type_pk


# Возвращает все категории с подкатегориями в виде списка кортежей с slug, name и списокм подкатегорий если он есть
# categories = [(slug, name, []),]
def get_categories(parent_id) -> list:
    categories = []
    queryset = Category.objects.filter(parent=parent_id)

    for cat in queryset:
        category = (cat.slug, cat.name, get_categories(cat.pk))
        categories.append(category)

    return categories


# находит отсортированные по дате неоплаченные(по умолчанию) заказы для всей корзины или только для конкретного id_messenger
def get_orders_for_user(user_pk: int, id_messenger: int = 0, paid: bool = False) -> models.QuerySet:
    orders = []
    params = {'user': user_pk, 'paid': paid}

    if id_messenger:
        params['id_messenger'] = id_messenger

    orderset = Order.objects.filter(**params).order_by('-time_update')

    if orderset.exists():
        orders = orderset

    return orders


# создает новую Корзину пользователя если ее ещё нет
def create_new_cart(new_cart_info: dict) -> dict:
    serializer = CartSerializer(data=new_cart_info)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    cart_info = serializer.data
    cart_info['products'] = []
    return cart_info


# получает или создает Корзину пользователя по ID пользователя в виде словаря
def get_cart_by_user_id(user_pk: int, for_anonymous_user: bool = False) -> dict:
    cart_info = {}
    cartset = Cart.objects.filter(user=user_pk).values()

    if cartset.exists():
        cart_info = cartset[0]
    else:
        new_cart_info = {
            'user': user_pk,
            'for_anonymous_user': for_anonymous_user
        }
        cart_info = create_new_cart(new_cart_info)

    return cart_info


# получает одну строку товара из Корзины или Заказа в виде объекта строки product_cart и в виде словаря product_cart_info
def get_cart_order_product(cart_order_pk: int, product_pk: int, id_messenger: int = 0, for_order: bool = False) -> tuple[CartProduct, dict]:
    product_cart = None
    product_cart_info = {}
    params = {'product': product_pk}

    if id_messenger:
        params['id_messenger'] = id_messenger

    if for_order:
        params['order'] = cart_order_pk
    else:
        params['cart'] = cart_order_pk

    queryset = CartProduct.objects.filter(**params)

    if queryset.exists():
        product_cart = queryset[0]
        product_cart_info = queryset.values()

    return product_cart, product_cart_info


# получает все строки из Корзины или Заказа в виде списка
# id_messenger - имеет значение только для выборки строк Корзины, иначе всегда 0
def get_cart_order_products(cart_order_pk: int, id_messenger: int = 0, for_order: bool = False) -> models.QuerySet:
    products_cart_order = []
    params = {}

    if id_messenger:
        params['id_messenger'] = id_messenger

    if for_order:
        params['order'] = cart_order_pk
    else:
        params['cart'] = cart_order_pk

    queryset = CartProduct.objects.filter(**params)

    if queryset.exists():
        products_cart_order = queryset

    return products_cart_order


def get_stock_product(product_pk: int, warehouse_pk: int) -> Decimal:
    stock = Decimal(0)
    params = {'product': product_pk, 'warehouse': warehouse_pk}

    queryset = StockProducts.objects.filter(**params)

    if queryset.exists():
        stock = Decimal(queryset[0].stock)

    return stock


# Проверяет достаточно ли товара для отгрузки, если всего хватает словарь нехватки будет пустым
# возвращает словарь нехватки {product_id: difference} где по каждому товару в словаре есть информация разности остатка и заказа
def check_stock_in_order(order_pk: int) -> dict:
    result = {}

    if not order_pk:
        result['error'] = False
        return result

    products_order = get_cart_order_products(order_pk, 0, True)

    for product_row in products_order:
        stock = get_stock_product(
            product_row.product_id, product_row.warehouse_id)

        if product_row.quantity > stock:
            result[product_row.product.name] = product_row.quantity - stock

    return result


# получает последнюю ценую и скидку
def get_last_price(product_pk: int) -> dict:
    price_info = {}
    priceset = Prices.objects.filter(product=product_pk).order_by(
        '-date_update').values('price', 'discount_percentage')

    if priceset.exists():
        price_info = priceset[0]

    return price_info


# Добавляет товар в корзину(создает её при необходимости) или изменяет количество товара как в большую так и меньшую сторону
# Если количество товара опускается до нуля, то строка удаляется
def add_delete_update_product_to_cart(user: AbstractBaseUser, request_data: dict) -> dict:
    user_pk = user.pk
    product_pk = request_data.get('product_pk', 0)
    warehouse_pk = request_data.get('warehouse_pk', 0)
    id_messenger = request_data.get('id_messenger', 0)
    for_anonymous_user = request_data.get('for_anonymous_user', False)

    if not product_pk or not warehouse_pk:
        data_response = {'error': 'product_pk or warehouse_pk is undefined'}
        return data_response

    cart_info = get_cart_by_user_id(user_pk, for_anonymous_user)
    cart_pk = cart_info.get('id', 0)

    price_info = get_last_price(product_pk)

    if not price_info:
        data_response = {'error': 'Price not found'}
        return data_response

    # Теперь заполним данные о новой строке товара в корзине
    new_cart_product = {
        'user': user_pk,
        'cart': cart_pk,
        'id_messenger': id_messenger,
        'quantity': Decimal(request_data['quantity']),
        'warehouse': warehouse_pk,
        'product': product_pk,
        'price': Decimal(price_info.get('price', 0.0)),
        'discount_percentage': int(price_info.get('discount_percentage', 0)),
    }

    # Строка товара для корзины готова, теперь попробуем найти строку с этим товаром в Корзине
    product_cart, product_cart_info = get_cart_order_product(
        cart_pk, product_pk, id_messenger)

    # если нашли строку в корзине с этим же товаром, пересчитаем количество и сумму, если нет, добавим новую строку или вообще не добавим ничего
    if product_cart:
        quantity = new_cart_product['quantity'] + product_cart.quantity

        if quantity <= 0:
            product_cart.delete()
            data_response = {'delete': 'Product delete from cart'}
        else:
            product_cart.quantity = quantity
            product_cart.save()
            data_response = product_cart_info
    # если создаём новую строку, то количество должно быть больше нуля
    elif new_cart_product['quantity'] > 0:
        serializer = CartProductCreateSerializer(data=new_cart_product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data_response = serializer.data
    else:
        data_response = {'error': 'quantity <= 0'}

    return data_response


# удаляет сразу весь товар из Корзины или Заказа, независимо от количества
def delete_product_from_cart_or_order(user: AbstractBaseUser, request_data: dict) -> dict:
    user_pk = user.pk
    product_pk = request_data.get('product_pk', 0)
    id_messenger = request_data.get('id_messenger', 0)
    order_pk = request_data.get('order_pk', 0)

    if not product_pk or not id_messenger:
        data_response = {'error': 'product_pk or id_messenger is undefined'}
        return data_response

    if order_pk:
        product_cart, _ = get_cart_order_product(
            order_pk, product_pk, id_messenger, True)
    else:
        for_anonymous_user = request_data.get('for_anonymous_user', False)
        cart_info = get_cart_by_user_id(user_pk, for_anonymous_user)
        cart_pk = cart_info.get('id', 0)
        product_cart, _ = get_cart_order_product(
            cart_pk, product_pk, id_messenger)

    if product_cart:
        product_cart.delete()
        data_response = {'delete': 'Product delete from cart'}
    else:
        data_response = {'error': 'Product not found in cart'}

    return data_response


# превращает строки Корзины в строки Заказа при оформлении Заказа из Корзины
# или добавляет их к существующему неоплаченному Заказу, пример тела POST
# {
#   "first_name": "Иван",
#   "last_name": "Иванов",
#   "phone": "79377777777",
#   "id_messenger": 827503364, <- опционально, если это Телеграм магазин
# }
def create_or_update_order(user: AbstractBaseUser, order_info: dict) -> dict:
    user_pk = user.pk
    id_messenger = order_info.get('id_messenger', 0)
    phone = order_info.get('phone', '')
    for_anonymous_user = order_info.get('for_anonymous_user', False)
    order_info['status'] = order_info.get('status_pk', get_default_status())
    order_info['delivery_type'] = order_info.get(
        'delivery_type_pk', get_default_delivery_type())
    order_info['payment_type'] = order_info.get(
        'payment_type_pk', get_default_payment_type())

    if not order_info['status']:
        return {'error': 'Status not found'}
    elif not order_info['delivery_type']:
        return {'error': 'DeliveryType not found'}
    elif not order_info['payment_type']:
        return {'error': 'PaymentType not found'}
    elif not phone:
        return {'error': 'Phone not found'}

    order_info['user'] = user_pk

    # найду последний неоплаченный заказ, что бы добавить в него новые товары из корзины или создам новый
    unpaid_orders = get_orders_for_user(user_pk, id_messenger, False)

    if unpaid_orders:
        order_instance = unpaid_orders[0]
        order_info['id'] = order_instance.pk
        order_info['quantity'] = order_instance.quantity
        order_info['discount'] = order_instance.discount
        order_info['amount'] = order_instance.amount
    else:
        serializer_order = OrderCreateSerializer(data=order_info)
        serializer_order.is_valid(raise_exception=True)
        serializer_order.save()
        order_info = serializer_order.data
        order_info['quantity'] = Decimal(0)
        order_info['discount'] = Decimal(0)
        order_info['amount'] = Decimal(0)
        order_instance = serializer_order.instance

    order_pk = order_info['id']
    cart_info = get_cart_by_user_id(user_pk, for_anonymous_user)
    cart_pk = cart_info.get('id', 0)

    # найду и превращу все строки Корзины в строки Заказа
    product_carts = get_cart_order_products(cart_pk, id_messenger)

    for product_cart in product_carts:
        # увеличу общие данные Заказа только для того, что бы вернуть их в ответе, расчет в самой БД делается сигналами
        order_info['quantity'] += product_cart.quantity
        order_info['discount'] += product_cart.discount
        order_info['amount'] += product_cart.amount

        # если найду строку с тем же товаром в текущем Заказе, то изменю количество в ней, а строку Корзины удалю
        order_row, _ = get_cart_order_product(
            order_pk, product_cart.product.pk, id_messenger, True)

        if order_row:
            order_row.quantity = order_row.quantity + product_cart.quantity
            order_row.save()
            product_cart.delete()
        else:
            # если строку не нашёл, то переделаю строку Корзины в строку Заказа
            product_cart.cart = None
            product_cart.order = order_instance
            product_cart.phone = phone
            product_cart.save()

    return order_info


# получает полную информацию о Заказе с товарами
def get_order_full_info(user: AbstractBaseUser, get_params: dict) -> dict:
    order_info = {}
    products = []

    if not get_params:
        return order_info

    user_pk = user.pk
    order_pk = get_params.get('order_pk', 0)
    id_messenger = get_params.get('id_messenger', '0')
    id_messenger = int(id_messenger) if id_messenger.isdigit() else 0
    paid = get_params.get('paid', None)

    update_price_in_cart_order(order_pk, id_messenger, True)

    params = {'user': user_pk, 'pk': order_pk}

    if paid is not None:
        params['paid'] = True if paid != '0' else False

    if id_messenger:
        params['id_messenger'] = id_messenger

    orderset = Order.objects.filter(**params)

    if orderset.exists():
        serializer_order = OrderSerializer(orderset[0])
        order_info = serializer_order.data
        products_order_set = CartProduct.objects.filter(order=order_pk)

        for product_order in products_order_set:
            serializer_row = CartProductSerializer(product_order)
            product_info = serializer_row.data

            # удалю лишнюю инфу о ценах и остатках товаров, сериализатор их выдает по умолчанию
            if 'get_prices' in product_info['product']:
                product_info['product'].pop('get_prices')

            if 'get_stock_product' in product_info['product']:
                product_info['product'].pop('get_stock_product')

            products.append(product_info)

        order_info['products'] = products

    return order_info


# получает полную информацию о Корзине с товарами
def get_cart_full_info(user: AbstractBaseUser, get_params: dict) -> dict:
    cart_info = {}
    products = []

    user_pk = user.pk
    for_anonymous_user = get_params.get('for_anonymous_user', False)
    id_messenger = get_params.get('id_messenger', '0')
    id_messenger = int(id_messenger) if id_messenger.isdigit() else 0

    cart_info = get_cart_by_user_id(user_pk, for_anonymous_user)
    cart_pk = cart_info.get('id', 0)

    # надо обновить строки и корзину если цены не совпадают
    update_price_in_cart_order(cart_pk, id_messenger, False)

    cartset = Cart.objects.filter(user=user_pk)

    if cartset.exists():
        serializer_cart = CartSerializer(cartset[0])
        cart_info = serializer_cart.data
        products_cart_set = cart_info['get_cart_products']

        for product_cart in products_cart_set:
            product_info = product_cart['product']
            if 'get_prices' in product_info:
                product_cart['product'].pop('get_prices')

            if 'get_stock_product' in product_info:
                product_cart['product'].pop('get_stock_product')

            if not id_messenger:
                products.append(product_cart)
            elif id_messenger == product_cart['id_messenger']:
                products.append(product_cart)

        cart_info['products'] = products
        cart_info.pop('get_cart_products')
    else:
        new_cart_info = {
            'user': user_pk,
            'for_anonymous_user': for_anonymous_user
        }
        cart_info = create_new_cart(new_cart_info)

    return cart_info


# проверяет актуальность цен в строках Заказа(Корзины) и обновляет данные строк и Заказа(Корзины) перед отправкой пользовтаелю
def update_price_in_cart_order(cart_order_pk: int, id_messenger: int = 0, for_order: bool = False) -> None:
    # проверю оплату Заказа, в оплаченных Заказах не нужно менять цены
    if for_order:
        orderset = Order.objects.filter(pk=cart_order_pk)

        if orderset.exists():
            if orderset[0].paid:
                return

    cart_products = get_cart_order_products(
        cart_order_pk, id_messenger, for_order)

    for product_row in cart_products:
        product_pk = product_row.product.pk
        price_info = get_last_price(product_pk)
        current_price = price_info.get('price', 0)
        current_discount_percentage = price_info.get('discount_percentage', 0)

        if product_row.price == current_price and product_row.discount_percentage == current_discount_percentage:
            continue

        product_row.price = current_price
        product_row.discount_percentage = current_discount_percentage
        product_row.save()
