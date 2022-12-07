from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser
from shop.serializers import *
from shop.models import *


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


def get_default_price_type() -> PriceType:
    price_type = None

    queryset = PriceType.objects.filter(default=True)

    if queryset.exists():
        price_type = queryset[0]

    return price_type


def get_default_currency() -> Currency:
    currency = None

    queryset = Currency.objects.filter(default=True)

    if queryset.exists():
        currency = queryset[0]

    return currency

# Возвращает рекурсивно все категории с подкатегориями в виде списка кортежей с slug, name и списокм подкатегорий если он есть
# categories = [(slug, name, []),]
def get_categories(parent_id) -> list:
    categories = []
    queryset = Category.objects.filter(parent=parent_id)

    for cat in queryset:
        category = (cat.slug, cat.name, get_categories(cat.pk))
        categories.append(category)

    return categories


# Возвращает список из всех родителей категории, в конце списка сама категория, а в начале корневой каталог
def get_parents_category(category_slug: str, parents: list) -> list[models.Model]:
    queryset = Category.objects.filter(slug=category_slug)

    if queryset.exists():
        category = queryset[0]
        parents.append(category)

        if category.parent is not None:
            get_parents_category(category.parent.slug, parents)

    return parents[::-1]


# Возвращает все цены товаров входящих непосредственно в данную категорию с ценами по умолчанию или пустой список
def get_products_prices_for_category(category_slug: str) -> models.QuerySet:
    price_products = Prices.objects.select_related('product', 'product__category', 'currency').filter(
        product__category__slug=category_slug, price_type__default=True)

    return price_products


# НЕИСПОЛЬЗУЕТСЯ УДАЛИТЬ Получает словарь товаров со списокм складов и остатков по ним
def get_products_stocks_for_category(category_slug: str) -> dict[list[dict]]:
    price_products = Prices.objects.select_related('product', 'product__category').filter(
        product__category__slug=category_slug, price_type__default=True)
    stock_products = StockProducts.objects.select_related('product', 'warehouse').filter(
        product__pk__in=price_products.values('product__pk'))

    stocks = {}

    for product_info in stock_products:
        current_product_pk = product_info.product.pk
        warehouses_products = []

        for product_info2 in stock_products:
            if product_info2.product.pk == current_product_pk:
                warehouses_products.append(
                    {'warehouse_pk': product_info2.warehouse.pk})
                warehouses_products.append(
                    {'warehouse_name': product_info2.warehouse.name})
                warehouses_products.append({'stock': product_info2.stock})

        stocks[product_info.product] = warehouses_products

    return stocks


# Возвращает всю необходимую информацию для списка товаров исходя из поиска по наименованию
def search_products(search_text: str):
    price_products = Prices.objects.select_related('product', 'product__category', 'currency').filter(
        product__name__icontains=search_text, price_type__default=True)

    return price_products


def get_attributes_product(product_pk: int) -> models.QuerySet:
    product_attributes = AttributeProductValues.objects.select_related(
        'attribute', 'value').filter(product=product_pk)

    return product_attributes


# Возвращает вложенные категории в корневую категорию и саму категорию
def get_nested_categories(category_slug: str) -> tuple[models.Model, models.QuerySet[Category]]:
    nested_categories = models.QuerySet(Category)
    categories = Category.objects.filter(slug=category_slug)

    if categories.exists():
        root_category = categories[0]
        nested_categories = root_category.nested_category.all()
    else:
        return (None, nested_categories)

    return (root_category, nested_categories)


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


# находит отсортированные по дате неоплаченные(по умолчанию) заказы по сессии
def get_orders_for_session(sessionid: str, paid: bool = False) -> models.QuerySet:
    orders = []
    params = {'sessionid': sessionid, 'paid': paid}

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

    if user_pk:
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


def get_cart_by_sessionid(session_key: str, for_anonymous_user: bool = False) -> dict:
    cart_info = {}

    if session_key:
        cartset = Cart.objects.filter(sessionid=session_key).values()

        if cartset.exists():
            cart_info = cartset[0]
        else:
            new_cart_info = {
                'sessionid': session_key,
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


# Получает остаток товара на одном складе
def get_stock_product(product_pk: int, warehouse_pk: int) -> Decimal:
    stock = Decimal(0)
    params = {'product': product_pk, 'warehouse': warehouse_pk}

    queryset = StockProducts.objects.filter(**params)

    if queryset.exists():
        stock = Decimal(queryset[0].stock)

    return stock


# Получает остаток товара по всем складам
def get_all_stock_product(product_pk: int) -> Decimal:
    stock = Decimal(0)
    params = {'product': product_pk}

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


# возвращает последнюю цену и скидку
def get_last_price(product_pk: int, price_type_pk: int = 0) -> dict:
    price_info = {}

    if not price_type_pk:
        price_type_pk = get_default_price_type()

    priceset = Prices.objects.filter(product=product_pk, price_type=price_type_pk).order_by(
        '-date_update').values('price', 'discount_percentage')

    if priceset.exists():
        price_info = priceset[0]

    return price_info


# создает новую Настройку пользователя если её ещё нет
def create_new_settings(new_settings_info: dict) -> UserSettings:
    settings = UserSettings(**new_settings_info)
    settings.save()
    return settings


# Получает или создает настройки пользователя
def get_settings_user(user: AbstractBaseUser) -> dict:
    settings_info = {}

    if not user.is_authenticated:
        settings_info = {
            'currency' : get_default_currency(),
            'price_type': get_default_price_type()
        }
        return settings_info

    cartset = UserSettings.objects.filter(user=user.pk)

    if cartset.exists():
        settings = cartset[0]
    else:
        settings_info = {
            'user': user,
            'currency' : get_default_currency(),
            'price_type': get_default_price_type()
        }
        settings = create_new_settings(settings_info)
    
    if not settings.currency:
        settings_info['currency'] = get_default_currency()

    if not settings.price_type:
        settings_info['price_type'] = get_default_price_type()

    return settings_info


# Добавляет товар в корзину(создает её при необходимости) или изменяет количество товара как в большую так и меньшую сторону
# Если количество товара опускается до нуля, то строка удаляется, так же получает актуальные цены
# Более умная функция нежели функция REST product_to_cart_update
def add_delete_update_product_to_cart(user: AbstractBaseUser, request_data: dict, session_key: str = '') -> dict:
    product_pk = request_data.get('product_pk', 0)
    warehouse_pk = request_data.get('warehouse_pk', None)
    id_messenger = request_data.get('id_messenger', 0)
    for_anonymous_user = request_data.get('for_anonymous_user', False)
    # Признак того что в AJAX запросе идет не увеличение/уменьшение количества товара, а установка нового количества
    set_new_quantity = request_data.get('set_new_quantity', False)

    if not product_pk:
        data_response = {'error': 'product_pk is undefined'}
        return data_response

    all_stock = get_all_stock_product(product_pk)

    if not all_stock:
        data_response = {'error': 'product is out of stock'}
        return data_response

    if user.is_authenticated:
        user_pk = user.pk
        cart_info = get_cart_by_user_id(user_pk, for_anonymous_user)
    elif session_key:
        cart_info = get_cart_by_sessionid(session_key, for_anonymous_user)
    else:
        data_response = {'error': 'user_pk and session_key is undefined'}
        return data_response

    cart_pk = cart_info.get('id', 0)

    # получим актуальные цены
    settings_user = get_settings_user(user)
    price_type_pk = settings_user.get('price_type', 0)
    price_info = get_last_price(product_pk, price_type_pk)

    if not price_info:
        data_response = {'error': 'Price not found'}
        return data_response

    # Теперь заполним данные о новой строке товара в корзине
    new_cart_product = {
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

    new_quantity = new_cart_product['quantity']

    # если это не установка нового количества, то прибавим его к текущему в строке корзины
    if product_cart and not set_new_quantity:
        new_quantity = product_cart.quantity + new_cart_product['quantity']

    # проверим не превышает ли количество в корзине/заказе общий остаток
    if new_quantity > all_stock:
        data_response = {'error': 'Excess balance of goods'}
        return data_response

    # если нашли строку в корзине с этим же товаром, пересчитаем количество и сумму, если нет, добавим новую строку или вообще не добавим ничего
    if product_cart:
        if new_quantity <= 0:
            product_cart.delete()
            data_response = {'delete': 'Product delete from cart'}
        else:
            product_cart.quantity = new_quantity
            product_cart.save()
            data_response = product_cart_info
    # если создаём новую строку, то количество должно быть больше нуля
    elif new_quantity > 0:
        serializer = CartProductCreateSerializer(data=new_cart_product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data_response = serializer.data
    else:
        data_response = {'error': 'quantity <= 0'}

    return data_response


# удаляет сразу весь товар из Корзины или Заказа, независимо от количества
def delete_product_from_cart_or_order(user: AbstractBaseUser, request_data: dict) -> dict:
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
        user_pk = user.pk
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
    id_messenger = order_info.get('id_messenger', 0)
    phone = order_info.get('phone', '')
    for_anonymous_user = order_info.get('for_anonymous_user', False)
    order_info['status'] = order_info.get('status_pk', get_default_status())
    order_info['delivery_type'] = order_info.get(
        'delivery_type_pk', get_default_delivery_type()
    )
    order_info['payment_type'] = order_info.get(
        'payment_type_pk', get_default_payment_type()
    )

    if not order_info['status']:
        return {'error': 'Status not found'}
    elif not order_info['delivery_type']:
        return {'error': 'DeliveryType not found'}
    elif not order_info['payment_type']:
        return {'error': 'PaymentType not found'}
    elif not phone:
        return {'error': 'Phone not found'}

    user_pk = user.pk if user.is_authenticated else 0
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
def get_order_full_info(user: AbstractBaseUser, get_params: dict = {}, session_key: str = '') -> dict:
    order_info = {}
    products = []

    if not get_params or (not user.is_authenticated and not session_key):
        return order_info

    order_pk = get_params.get('order_pk', 0)
    id_messenger = get_params.get('id_messenger', '0')
    id_messenger = int(id_messenger) if id_messenger.isdigit() else 0
    paid = get_params.get('paid', None)

    user_pk = user.pk if user.is_authenticated else 0
    settings_user = get_settings_user(user)
    price_type_pk = settings_user.get('price_type', 0)

    update_price_in_cart_order(order_pk, id_messenger, True, price_type_pk)

    params = {'pk': order_pk}

    if user_pk:
        params['user'] = user_pk

    if session_key:
        params['sessionid'] = session_key

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


def delete_cart_by_session_key(session_key: str) -> None:
    queryset = Cart.objects.filter(sessionid=session_key)

    if queryset.exists():
        cart = queryset[0]
        cart.delete()


def merging_two_shopping_carts(user: AbstractBaseUser, session_key: str) -> None:
    anonymous_cart_products = CartProduct.objects.filter(
        cart__sessionid=session_key).values()
    new_product_cart = {}

    for product_cart in anonymous_cart_products:
        new_product_cart['product_pk'] = product_cart.get('product_id')
        new_product_cart['warehouse_pk'] = product_cart.get('warehouse_id')
        new_product_cart['id_messenger'] = product_cart.get('id_messenger')
        new_product_cart['quantity'] = product_cart.get('quantity')
        add_delete_update_product_to_cart(user, new_product_cart, session_key)

    delete_cart_by_session_key(session_key)


# получает полную информацию о Корзине с товарами с обновленными ценами
def get_cart_full_info(user: AbstractBaseUser, get_params: dict = {}, session_key: str = '') -> dict:
    products = []
    cart_info = {'quantity': 0, 'amount': 0, 'products': products}

    if not user.is_authenticated and not session_key:
        return cart_info

    user_pk = user.pk if user.is_authenticated else 0
    for_anonymous_user = get_params.get('for_anonymous_user', False)
    id_messenger = get_params.get('id_messenger', '0')
    id_messenger = int(id_messenger) if id_messenger.isdigit() else 0

    if user_pk:
        cart_info = get_cart_by_user_id(user_pk, for_anonymous_user)
        cartset = Cart.objects.filter(user=user_pk)
    else:
        cart_info = get_cart_by_sessionid(session_key, for_anonymous_user)
        cartset = Cart.objects.filter(sessionid=session_key)

    cart_pk = cart_info.get('id', 0)
    settings_user = get_settings_user(user)
    price_type_pk = settings_user.get('price_type', 0)

    # надо обновить строки и корзину если цены не совпадают
    update_price_in_cart_order(cart_pk, id_messenger, False, price_type_pk)

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
    elif user_pk:
        new_cart_info = {
            'user': user_pk,
            'for_anonymous_user': for_anonymous_user
        }
        cart_info = create_new_cart(new_cart_info)
    elif session_key:
        new_cart_info = {
            'sessionid': session_key,
            'for_anonymous_user': for_anonymous_user
        }
        cart_info = create_new_cart(new_cart_info)

    return cart_info


# проверяет актуальность цен в строках Заказа(Корзины) и обновляет данные строк и Заказа(Корзины) перед отправкой пользователю
def update_price_in_cart_order(cart_order_pk: int, id_messenger: int = 0, for_order: bool = False, price_type_pk: int = 0) -> None:
    # проверю оплату Заказа, в оплаченных Заказах не нужно менять цены
    if for_order:
        orderset = Order.objects.filter(pk=cart_order_pk)

        if orderset.exists() and orderset[0].paid:
            return

    cart_products = get_cart_order_products(
        cart_order_pk, id_messenger, for_order)

    for product_row in cart_products:
        product_pk = product_row.product.pk
        price_info = get_last_price(product_pk, price_type_pk)
        current_price = price_info.get('price', 0)
        current_discount_percentage = price_info.get('discount_percentage', 0)

        if product_row.price == current_price and product_row.discount_percentage == current_discount_percentage:
            continue

        product_row.price = current_price
        product_row.discount_percentage = current_discount_percentage
        product_row.save()


def get_favorite_products_info(user: AbstractBaseUser) -> dict:
    products = []
    wishlist = {'count': 0, 'there_discounts': False, 'products': products}

    if not user.is_authenticated:
        return wishlist

    user_pk = user.pk

    favorite_products = FavoriteProduct.objects.select_related(
        'product').filter(user=user_pk)

    # тут лучше вручную сериализовать данные
    for favorite_product in favorite_products:
        price_info = get_last_price(favorite_product.product.pk)

        if price_info['discount_percentage']:
            # зафиксирую что в наборе товаров есть хоть одна скидка
            wishlist['there_discounts'] = True

        row_product = {}
        row_product['pk'] = favorite_product.pk
        row_product['name'] = favorite_product.product.name
        row_product['price'] = price_info['price']
        row_product['discount_percentage'] = price_info['discount_percentage']
        row_product['slug'] = favorite_product.product.slug
        row_product['photo'] = favorite_product.product.photo.url
        products.append(row_product)

    wishlist['count'] = favorite_products.count()
    wishlist['products'] = products

    return wishlist


def add_favorite_product(user: AbstractBaseUser, favorite_product: dict) -> dict:
    if not user.is_authenticated:
        return {'error': 'User not found'}

    user_pk = user.pk
    favorite_product['user'] = user_pk

    # определим, есть ли уже этот товар в списке желаемых
    queryset = FavoriteProduct.objects.filter(**favorite_product)

    if queryset.exists():
        return favorite_product

    # усли нет, то добавим новую строку
    serializer_order = FavoriteProductCreateSerializer(data=favorite_product)
    serializer_order.is_valid(raise_exception=True)
    serializer_order.save()
    favorite_product = serializer_order.data

    return favorite_product
