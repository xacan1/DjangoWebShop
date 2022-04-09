from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):

    # Диспетчер пользовательских моделей, в котором email используется для аутентификации вместо username.
    # Создание и запись пользователя  и суперпользователя с email и password

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, unique=True,
                             blank=True, verbose_name='Телефон')
    # orders = models.ManyToManyField(
    #     'Order', related_name='related_orders', verbose_name='Заказы покупателя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Модель магазина:
# Категория
# Бренд
# Товар(продукт)
# Спецификации (несколько таблиц по типам данных: числа, строки, булево)
# Строка товара в корзине
# Корзина
# Пользователь - стандартная модель User из Django


User = get_user_model()


def product_image_path(instance, filename):
    return f'photos/{instance.slug}/{filename}'


# Категории - это корневые папки справочника Номенклатура в 1С
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    external_code = models.CharField(
        max_length=11, unique=True, verbose_name='Внешний код')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to=product_image_path,
                              verbose_name='Изображение')
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Создан')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Доступен к покупке')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='get_products', verbose_name='Категория')
    external_code = models.CharField(max_length=11,
                                     unique=True, verbose_name='Внешний код')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)


# сами названия атрибутов (свойств) товаров
class Attribute(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='Атрибут')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'


# Назначение атрибутов для категорий, у каждой категории свой набор атрибутов
# В дальнейшем нужно быдет сделать форму для заполнения категорий у товаров на сайте,
# с фильтрацией по этой таблице, что бы видеть какие именно атрибуты есть у всех товаров данной категории
class AttributeCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='get_attributes', verbose_name='Категория')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,
                                  related_name='get_categories', verbose_name='Атрибут')

    def __str__(self) -> str:
        return f'Атрибут {self.attribute.name} для {self.category.name}'

    class Meta:
        verbose_name = 'Назначение атрибута для категории'
        verbose_name_plural = 'Назначение атрибутов для категорий'


# Связка товара, атрибутов и конкретных значений
# Значениями атрибутов пока что будут строки
class AttributeProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='get_attributes', verbose_name='Товар')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,
                                  related_name='get_products', verbose_name='Атрибут')
    value = models.CharField(max_length=100, verbose_name='Значение атрибута')

    def __str__(self) -> str:
        return f'Атрибут {self.attribute.name} = {self.value} для {self.product.name}'

    class Meta:
        verbose_name = 'Значение атрибута для товара'
        verbose_name_plural = 'Значения атрибутов для товаров'


class Prices(models.Model):
    price = models.DecimalField(max_digits=15,
                                decimal_places=2, verbose_name='Цена')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='get_prices', verbose_name='Товар')
    date_update = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата установки цены')
    discount_percentage = models.DecimalField(max_digits=3, decimal_places=0,
                                              default=0, verbose_name='Скидка %')

    def __str__(self) -> str:
        return f'Цена {self.product.name} = {self.price}'

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


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


# Строка в корзине товаров, превращается в строку заказа когда корзина прикрепляется к заказу
# discount - скидка в деньгах на всю строку, а не на штуку товара
# тут или товар на пользователе или товар на id_anonymous(ID из мессенджера), если товар покупается из телеграма
# id_anonymous - по сути специальный разрез учета по номеру телефона для подкорзины телеграм бота,
# что бы отделить товар одного покупателя от другого в общей корзине телеграм бота
class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Покупатель')
    id_anonymous = models.IntegerField(default=0,
                                       verbose_name='ID из мессенджера')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE,
                             related_name='get_cart_products', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Товар')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  verbose_name='Склад')
    quantity = models.DecimalField(max_digits=15, decimal_places=3,
                                   default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=15, decimal_places=2,
                                default=0, verbose_name='Цена')
    discount = models.DecimalField(max_digits=15, decimal_places=2,
                                   default=0, verbose_name='Скидка')
    discount_percentage = models.DecimalField(max_digits=3, decimal_places=0,
                                              default=0, verbose_name='Скидка %')
    amount = models.DecimalField(max_digits=15, decimal_places=2,
                                 default=0, verbose_name='Сумма')

    def __str__(self) -> str:
        return f'Товар в корзине {self.product.name} в количестве {self.quantity}'

    class Meta:
        verbose_name = 'Строка товара в корзине'
        verbose_name_plural = 'Строки товаров в корзинах'


# Корзина товаров покупателя сайта, один аккаунт может иметь только одну корзину, а телеграм бот является
# посредником между телеграм пользователем и БД сайта и получается, что имеет корзину общую для всех его
# пользователей телеги. Раз корзина бота это помойка товаров разных людей, то разделять такие "подкорзины"
# нужно по ID пользователей из месседжера.
# for_anonymous_user - признак что этот пользователь сайта является общим пользователем для АПИ и его корзина
# общая для всех покупателей заказывающих через него
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='get_user_cart', verbose_name='Покупатель')
    # cart_products = models.ManyToManyField(CartProduct, blank=True,
    #                                        related_name='get_cart', verbose_name='Товары')
    quantity = models.DecimalField(max_digits=15, decimal_places=3,
                                   default=0, verbose_name='Общее количество')
    amount = models.DecimalField(max_digits=15, decimal_places=2,
                                 default=0, verbose_name='Общая сумма')
    discount = models.DecimalField(max_digits=15, decimal_places=2,
                                   default=0, verbose_name='Общая скидка')
    in_order = models.BooleanField(default=False, verbose_name='В заказе')
    for_anonymous_user = models.BooleanField(default=False,
                                             verbose_name='Анонимный покупатель')

    def __str__(self) -> str:
        return f'Корзина пользователя {self.user.email}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


# id_anonymous необязательное поле, нужно только если заказ анонимный, по этому полю осуществляется связь строк корзины и анонимного заказа
# например из телеграм бота, где пользолватель не имея учетки на сайте сам вводит свои данные в заказе
# phone при анонимном заказе заполняется при получении телефона ботом, иначе из учетки на сайте
class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )

    castomer = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='get_orders', verbose_name='Покупатель')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             null=True, blank=True, verbose_name='Корзина')
    id_anonymous = models.IntegerField(default=0,
                                       verbose_name='ID из мессенджера')
    address = models.CharField(max_length=1024,
                               null=True, blank=True, verbose_name='Адрес')
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата изменения')
    order_date = models.DateField(default=timezone.now,
                                  verbose_name='Желаемая дата получения')
    comment = models.TextField(null=True,
                               blank=True, verbose_name='Комментарий к заказу')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,
                              default=STATUS_NEW, verbose_name='Статус заказа')
    buying_type = models.CharField(max_length=100, choices=BUYING_TYPE_CHOICES,
                                   default=BUYING_TYPE_SELF, verbose_name='Способ получения')
    # здесь этот номер уникален лишь в пределах 1 года как в 1С
    number = models.CharField(max_length=11, verbose_name='Номер заказа')

    def __str__(self) -> str:
        return f'Заказ {self.number} от {self.time_update}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-time_create',)
