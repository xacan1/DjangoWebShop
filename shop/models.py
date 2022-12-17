from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone, datetime_safe
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import unique_slugify
from rest_framework.authtoken.models import Token


User = get_user_model()


def product_image_path(instance, filename):
    return f'photos/{instance.slug}/{filename}'


def get_path_to_image(instance, filename):
    return f'photos/{instance.product.slug}/{filename}'


# Категории - это корневые папки справочника Номенклатура в 1С
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(max_length=255, unique=True)
    external_code = models.CharField(max_length=11, unique=True,
                                     verbose_name='Внешний код')
    photo = models.ImageField(upload_to=product_image_path, null=True,
                              blank=True, verbose_name='Изображение')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, default=None,
                               null=True, blank=True, related_name='nested_category',
                               verbose_name='Родитель')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name, allow_unicode=True)

        # self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('parent__name', 'name',)


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True,
                                   verbose_name='Описание')
    photo = models.ImageField(null=True, blank=True,
                              verbose_name='Основное изображение')
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Создан')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    is_published = models.BooleanField(default=True, blank=True,
                                       verbose_name='Доступен к покупке')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='get_products', verbose_name='Категория')
    external_code = models.CharField(max_length=11,
                                     unique=True, verbose_name='Внешний код')
    is_service = models.BooleanField(default=False, verbose_name='Услуга')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name, allow_unicode=True)

        # self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = (
            models.Index(fields=('id', 'slug')),
        )


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='get_images', verbose_name='Товар')
    photo = models.ImageField(upload_to=get_path_to_image,
                              verbose_name='Изображение')
    description = models.CharField(max_length=100, verbose_name='Описание')
    default = models.BooleanField(default=False, blank=True,
                                  verbose_name='Основное')

    def __str__(self) -> str:
        return f'Изображение {self.product.name} - {self.photo}'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'


# таблица для избранных товаров как в разрезе пользовтаелей сайта так и в разрезе ID телеграмма
class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Товар')
    id_messenger = models.IntegerField(default=0, blank=True,
                                       verbose_name='ID из мессенджера')

    def __str__(self) -> str:
        return f'{self.product.name} в избранном у {self.user.email} с id messenger: {self.id_messenger}'

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


# сами названия атрибутов (свойств) товаров из 1С, соответствует справочнику омАтрибутыТоваров
# Каждый атрибут связан с категорией (группой номенклатуры) товаров, ведь у каждой группы товаров свой набор атрибутов, за ичключением общих для всех атрибутов.
# например материал, объем ОЗУ, размер экрана. Свойства могут совпадать по названию, но каждое все равно уникально для группы товаров
class Attribute(models.Model):
    name = models.CharField(max_length=255, verbose_name='Атрибут')
    description = models.TextField(default='', blank=True,
                                   verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='get_attributes_category', verbose_name='Категория')
    external_code = models.CharField(max_length=11, unique=True,
                                     verbose_name='Внешний код')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'


# Значения для атрибутов из 1С, соответствует справочнику омЗначенияАтрибутовТоваров
# для каждого атрибута мы имеем некий набор значений, например объемы ОЗУ: 4, 8, 16 Гб
# значение может быть как строковым (name), оно обязательно, так и числовым (если числовое представление имеет смысл)
class AttributeValues(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,
                                  related_name='get_values', verbose_name='Атрибут')
    string_value = models.CharField(max_length=100,
                                    verbose_name='Строковое значение')
    numeric_value = models.DecimalField(max_digits=15, decimal_places=3,
                                        default=0, verbose_name='Числовое значение')
    external_code = models.CharField(max_length=11, unique=True,
                                     verbose_name='Внешний код')

    def __str__(self) -> str:
        return f'{self.string_value} ({self.attribute.name})'

    class Meta:
        verbose_name = 'Значение атрибута'
        verbose_name_plural = 'Значения атрибута'


# Связка товара, атрибутов и конкретных значений из регистра сведений 1С омЗначенияАтрибутовТоваров
# Значениями атрибутов пока что будут строки
class AttributeProductValues(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='get_attributes_product', verbose_name='Товар')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,
                                  verbose_name='Атрибут')
    value = models.ForeignKey(AttributeValues, on_delete=models.CASCADE,
                              verbose_name='Значение атрибута')

    def __str__(self) -> str:
        return f'Атрибут {self.attribute.name} = {self.value} для {self.product.name}'

    class Meta:
        verbose_name = 'Значение атрибута для товара'
        verbose_name_plural = 'Значения атрибутов для товаров'


class Currency(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Наименование')
    abbreviation = models.CharField(max_length=3,
                                    verbose_name='Аббревиатура')
    digital_code = models.IntegerField(default=0, blank=True,
                                       verbose_name='Цифровой код')
    sign = models.CharField(default='', max_length=5,
                            verbose_name='Знак')
    default = models.BooleanField(default=False, blank=True,
                                  verbose_name='Валюта по умолчанию')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class PriceType(models.Model):
    name = models.CharField(max_length=25, verbose_name='Наименование')
    external_code = models.CharField(max_length=11,
                                     unique=True, verbose_name='Внешний код')
    default = models.BooleanField(default=False, blank=True,
                                  verbose_name='Тип цен по умолчанию')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Тип цены'
        verbose_name_plural = 'Типы цен'


class Prices(models.Model):
    price = models.DecimalField(max_digits=15,
                                decimal_places=2, verbose_name='Цена')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='get_prices', verbose_name='Товар')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                 verbose_name='Валюта')
    price_type = models.ForeignKey(PriceType, on_delete=models.CASCADE,
                                   verbose_name='Тип цены')
    date_update = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата установки цены')
    discount_percentage = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                              validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка %')

    def __str__(self) -> str:
        return f'Цена {self.product.name} = {self.price}'

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        ordering = ('-date_update', )


class Warehouse(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    country = models.CharField(max_length=100, verbose_name='Страна')
    province = models.CharField(max_length=100,
                                verbose_name='Провинция(область)')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=255,
                               unique=True, verbose_name='Адрес')
    external_code = models.CharField(max_length=11,
                                     unique=True, verbose_name='Внешний код')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class StockProducts(models.Model):
    stock = models.DecimalField(max_digits=15,
                                decimal_places=3, verbose_name='Остаток')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='get_stock_product', verbose_name='Товар')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  related_name='get_stock_warehouse', verbose_name='Склад')

    def __str__(self) -> str:
        return f'Остаток {self.product.name} = {self.stock} на складе {self.warehouse.name}'

    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'


# дополнительные значения для пользователей, которые не вошли в основную модель
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='get_settings', verbose_name='Покупатель')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT,
                                 default=None, blank=True, null=True, verbose_name='Валюта')
    price_type = models.ForeignKey(PriceType, on_delete=models.PROTECT,
                                   default=None, blank=True, null=True, verbose_name='Тип цены')

    def __str__(self) -> str:
        return f'Настройки для {self.user.email}'

    class Meta:
        verbose_name = 'Настройка пользователя'
        verbose_name_plural = 'Настройки пользователей'


# Строка в корзине товаров, превращается в строку заказа когда строка прикрепляется к заказу,
# изначально order=null, а затем становится cart=null, когда заказ появляется
# discount - скидка в деньгах на всю строку, а не на штуку товара
# тут или товар на пользователе или товар на id_messenger(ID из мессенджера), если товар покупается из телеграма
# id_anonymous - по сути специальный разрез учета по номеру телефона для подкорзины телеграм бота,
# что бы отделить товар одного покупателя от другого в общей корзине телеграм бота
# phone - заполняется когда строка корзины превращается в строку заказа
# warehouse - не обязательное поле, нужно для учета в 1С, но можно и обойтись для ЗаказаПокупателя
class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE,
                             related_name='get_cart_products', null=True,
                             blank=True, verbose_name='Корзина')
    order = models.ForeignKey('Order', on_delete=models.CASCADE,
                              related_name='get_order_products', null=True,
                              blank=True, verbose_name='Заказ')
    id_messenger = models.IntegerField(default=0, blank=True,
                                       verbose_name='ID из мессенджера')
    phone = models.CharField(max_length=15, default='', blank=True,
                             verbose_name='Телефон')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Товар')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  null=True, blank=True, verbose_name='Склад (магазин)')
    quantity = models.DecimalField(max_digits=15, decimal_places=3,
                                   default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=15, decimal_places=2,
                                default=0, verbose_name='Цена')
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                   blank=True, verbose_name='Скидка')
    discount_percentage = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                              validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка %')
    amount = models.DecimalField(max_digits=15, decimal_places=2,
                                 default=0, verbose_name='Сумма')

    def __str__(self) -> str:
        return f'Товар в корзине {self.product.name} в количестве {self.quantity}'

    class Meta:
        verbose_name = 'Строка товара в корзине или заказе'
        verbose_name_plural = 'Строки товаров в корзинах или заказах'


# Корзина товаров покупателя сайта, один аккаунт может иметь только одну корзину, а телеграм бот является
# посредником между телеграм пользователем и БД сайта и получается, что имеет корзину общую для всех его
# пользователей телеги. Раз корзина бота это помойка товаров разных людей, то разделять такие "подкорзины"
# нужно по ID пользователей из месседжера.
# for_anonymous_user - признак что этот пользователь сайта является общим пользователем для АПИ и его корзина
# общая для всех покупателей заказывающих через него
# Корзина может быть не связана с пользователем (анонимная), но тогда она привязана к ID сессии, как только пользователь
# залогинится на сайт, сама корзина и товары из корзины сессии удалятся и перейдут в корзину пользователя
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='get_user_cart', verbose_name='Покупатель')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                 verbose_name='Валюта корзины')
    sessionid = models.CharField(max_length=40, default='', blank=True,
                                 verbose_name='Ключ сессии')
    quantity = models.DecimalField(max_digits=15, decimal_places=3, blank=True,
                                   default=0, verbose_name='Общее количество')
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True,
                                 default=0, verbose_name='Общая сумма')
    discount = models.DecimalField(max_digits=15, decimal_places=2, blank=True,
                                   default=0, verbose_name='Общая скидка')
    for_anonymous_user = models.BooleanField(default=False, blank=True,
                                             verbose_name='Анонимный покупатель')

    def __str__(self) -> str:
        return f'Корзина {self.user.email if self.user else self.sessionid}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


# Контрагент всегда привязан к пользователю, пользователь может существовать сам по себе, а один или несколько контрагентов всегда привязаны к пользователю
class Contractor(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    full_name = models.CharField(max_length=512, default='', blank=True,
                                 verbose_name='Официальное наименование')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, default='', blank=True,
                           verbose_name='КПП')
    registered_address = models.CharField(max_length=1024, default='',
                                          blank=True, verbose_name='Юридический адрес')
    actual_address = models.CharField(max_length=1024, default='', blank=True,
                                      verbose_name='Фактический адрес')

    def __str__(self) -> str:
        return f'Контрагент: {self.name}'

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class ContractorUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='get_contractors', verbose_name='Покупатель')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE,
                                   verbose_name='Контрагент')

    def __str__(self) -> str:
        return f'Контрагент: {self.contractor.name} пользователя: {self.user.email}'

    class Meta:
        verbose_name = 'Контрагент пользователя'
        verbose_name_plural = 'Контрагенты пользователей'


# for_bot - что бы любой бот знал что ему надо выбирать в заказе
class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус заказа')
    external_code = models.CharField(max_length=11,
                                     unique=True, verbose_name='Внешний код')
    for_bot = models.BooleanField(default=False,
                                  verbose_name='Для бота магазина')
    use = models.BooleanField(default=True, verbose_name='Использовать')

    def __str__(self) -> str:
        return f'Статус заказа: {self.name}'

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class PaymentType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Вид оплаты')
    external_code = models.CharField(max_length=11,
                                     unique=True, verbose_name='Внешний код')
    for_bot = models.BooleanField(default=False,
                                  verbose_name='Для бота магазина')
    use = models.BooleanField(default=True, verbose_name='Использовать')

    def __str__(self) -> str:
        return f'Вид оплаты: {self.name}'

    class Meta:
        verbose_name = 'Вид оплаты'
        verbose_name_plural = 'Виды оплат'


class DeliveryType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Способ получения')
    external_code = models.CharField(max_length=11,
                                     unique=True, verbose_name='Внешний код')
    for_bot = models.BooleanField(default=False,
                                  verbose_name='Для бота магазина')
    use = models.BooleanField(default=True, verbose_name='Использовать')

    def __str__(self) -> str:
        return f'Способ получения: {self.name}'

    class Meta:
        verbose_name = 'Способ получения'
        verbose_name_plural = 'Способы получения'


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True,
                            verbose_name='Номер купона')
    valid_from = models.DateTimeField(verbose_name='Действует с')
    valid_to = models.DateTimeField(verbose_name='Действует до')
    discount_percentage = models.DecimalField(max_digits=3, decimal_places=0,
                                              validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка %')
    active = models.BooleanField(verbose_name='Активен')
    external_code = models.CharField(max_length=11, default='', blank=True,
                                     verbose_name='Внешний код')

    def __str__(self) -> str:
        return f'Купон {self.code} на {self.discount_percentage}%'

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'


# id_messenger необязательное поле, нужно только если заказ из мессенджера, по этому полю осуществляется связь строк корзины и заказа
# например из телеграм бота, где пользолватель не имея учетки на сайте сам вводит свои данные в заказе
# sessionid - необязательное поле, если заказ с сайта от анонимного пользователя
# phone при анонимном заказе заполняется при получении телефона ботом, иначе из учетки на сайте
# в 1С заказ будет загружаться и в документе будет сохраняться pk заказа
# warehouse - не обязательное поле так как ЗаказПокупателя может быть сформирован и без него
class Order(models.Model):
    # STATUS_NEW = 'new'
    # STATUS_IN_PROGRESS = 'in_progress'
    # STATUS_READY = 'is_ready'
    # STATUS_COMPLETED = 'completed'
    # STATUS_CANCELLED = 'canceled'

    # DELIVERY_TYPE_SELF = 'self'
    # DELIVERY_TYPE_DELIVERY = 'delivery'

    # PAYMENT_TYPE_CASH = 'cash'
    # PAYMENT_TYPE_CARD = 'card'
    # PAYMENT_TYPE_ONLINE = 'online'

    # PAYMENT_TYPES = (
    #     (PAYMENT_TYPE_CASH, 'Наличная оплата'),
    #     (PAYMENT_TYPE_CARD, 'Оплата банковской картой'),
    #     (PAYMENT_TYPE_ONLINE, 'Онлайн оплата'),
    # )

    # STATUS_CHOICES = (
    #     (STATUS_NEW, 'Новый заказ'),
    #     (STATUS_IN_PROGRESS, 'Заказ в обработке'),
    #     (STATUS_READY, 'Заказ готов'),
    #     (STATUS_COMPLETED, 'Заказ выполнен'),
    #     (STATUS_CANCELLED, 'Заказ отменен'),
    # )

    # DELIVERY_TYPE_CHOICES = (
    #     (DELIVERY_TYPE_SELF, 'Самовывоз'),
    #     (DELIVERY_TYPE_DELIVERY, 'Доставка'),
    # )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True, related_name='get_orders', verbose_name='Покупатель')
    sessionid = models.CharField(max_length=40, default='', blank=True,
                                 verbose_name='Ключ сессии')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                 verbose_name='Валюта заказа')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    email = models.EmailField(max_length=254, default='', blank=True,
                              verbose_name='Email')
    id_messenger = models.IntegerField(default=0, blank=True,
                                       verbose_name='ID из мессенджера')
    address = models.CharField(max_length=1024, default='', blank=True,
                               verbose_name='Адрес доставки')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  null=True, blank=True, verbose_name='Склад (магазин) отгрузки')
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата изменения')
    delivery_date = models.DateField(default=datetime_safe.date.today,
                                     verbose_name='Плановая дата доставки')
    comment = models.TextField(default='', blank=True,
                               verbose_name='Комментарий к заказу')
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               verbose_name='Статус заказа')
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.PROTECT,
                                      verbose_name='Способ получения')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT,
                                     verbose_name='Вид оплаты')
    quantity = models.DecimalField(max_digits=15, decimal_places=3, blank=True,
                                   default=0, verbose_name='Общее количество')
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True,
                                 default=0, verbose_name='Общая сумма')
    discount = models.DecimalField(max_digits=15, decimal_places=2, blank=True,
                                   default=0, verbose_name='Общая скидка')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    canceled = models.BooleanField(default=False, verbose_name='Отменен')
    coupon = models.ForeignKey(Coupon, null=True, blank=True,
                               on_delete=models.SET_NULL, verbose_name='Купон')
    # номер уникален в пределах 1 года как в 1С, заполняется когда 1С загрузит заказ и вернет назад свой код документа
    external_code = models.CharField(max_length=11, default='', blank=True,
                              verbose_name='Внешний номер')

    def __str__(self) -> str:
        return f'Заказ №{self.pk} от {self.time_update.strftime("%d.%m.%Y")}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-time_create',)
