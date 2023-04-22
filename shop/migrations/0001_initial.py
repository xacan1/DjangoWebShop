# Generated by Django 4.1.8 on 2023-04-22 14:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.datetime_safe
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Атрибут')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('external_code', models.CharField(max_length=11, unique=True, verbose_name='Внешний код')),
            ],
            options={
                'verbose_name': 'Атрибут',
                'verbose_name_plural': 'Атрибуты',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionid', models.CharField(blank=True, default='', max_length=40, verbose_name='Ключ сессии')),
                ('quantity', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=15, verbose_name='Общее количество')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, verbose_name='Общая сумма')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, verbose_name='Общая скидка')),
                ('for_anonymous_user', models.BooleanField(blank=True, default=False, verbose_name='Анонимный покупатель')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя категории')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('external_code', models.CharField(max_length=11, unique=True, verbose_name='Внешний код')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=shop.models.product_image_path, verbose_name='Изображение')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nested_category', to='shop.category', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('parent__name', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('full_name', models.CharField(blank=True, default='', max_length=512, verbose_name='Официальное наименование')),
                ('inn', models.CharField(max_length=12, verbose_name='ИНН')),
                ('kpp', models.CharField(blank=True, default='', max_length=9, verbose_name='КПП')),
                ('registered_address', models.CharField(blank=True, default='', max_length=1024, verbose_name='Юридический адрес')),
                ('actual_address', models.CharField(blank=True, default='', max_length=1024, verbose_name='Фактический адрес')),
            ],
            options={
                'verbose_name': 'Контрагент',
                'verbose_name_plural': 'Контрагенты',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Номер купона')),
                ('valid_from', models.DateTimeField(verbose_name='Действует с')),
                ('valid_to', models.DateTimeField(verbose_name='Действует до')),
                ('discount_percentage', models.DecimalField(decimal_places=0, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка %')),
                ('for_discount', models.BooleanField(verbose_name='Скидочный')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Сумма')),
                ('active', models.BooleanField(verbose_name='Активен')),
                ('external_code', models.CharField(blank=True, default='', max_length=11, verbose_name='Внешний код')),
            ],
            options={
                'verbose_name': 'Купон',
                'verbose_name_plural': 'Купоны',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('abbreviation', models.CharField(max_length=3, verbose_name='Аббревиатура')),
                ('digital_code', models.IntegerField(blank=True, default=0, verbose_name='Цифровой код')),
                ('sign', models.CharField(default='', max_length=5, verbose_name='Знак')),
                ('default', models.BooleanField(blank=True, default=False, verbose_name='Валюта по умолчанию')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
            },
        ),
        migrations.CreateModel(
            name='DeliveryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Способ получения')),
                ('external_code', models.CharField(max_length=11, unique=True, verbose_name='Внешний код')),
                ('for_bot', models.BooleanField(default=False, verbose_name='Для бота магазина')),
                ('use', models.BooleanField(default=True, verbose_name='Использовать')),
            ],
            options={
                'verbose_name': 'Способ получения',
                'verbose_name_plural': 'Способы получения',
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Вид оплаты')),
                ('external_code', models.CharField(max_length=11, unique=True, verbose_name='Внешний код')),
                ('for_bot', models.BooleanField(default=False, verbose_name='Для бота магазина')),
                ('use', models.BooleanField(default=True, verbose_name='Использовать')),
            ],
            options={
                'verbose_name': 'Вид оплаты',
                'verbose_name_plural': 'Виды оплат',
            },
        ),
        migrations.CreateModel(
            name='PriceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Наименование')),
                ('external_code', models.CharField(max_length=11, unique=True, verbose_name='Внешний код')),
                ('default', models.BooleanField(blank=True, default=False, verbose_name='Тип цен по умолчанию')),
            ],
            options={
                'verbose_name': 'Тип цены',
                'verbose_name_plural': 'Типы цен',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Основное изображение')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('is_published', models.BooleanField(blank=True, default=True, verbose_name='Доступен к покупке')),
                ('external_code', models.CharField(max_length=11, unique=True, verbose_name='Внешний код')),
                ('is_service', models.BooleanField(default=False, verbose_name='Услуга')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_products', to='shop.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Статус заказа')),
                ('external_code', models.CharField(max_length=11, unique=True, verbose_name='Внешний код')),
                ('for_bot', models.BooleanField(default=False, verbose_name='Для бота магазина')),
                ('use', models.BooleanField(default=True, verbose_name='Использовать')),
            ],
            options={
                'verbose_name': 'Статус заказа',
                'verbose_name_plural': 'Статусы заказов',
            },
        ),
        migrations.CreateModel(
            name='UnitMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('short_name', models.CharField(max_length=25, verbose_name='Краткое наименование')),
                ('international_short_name', models.CharField(max_length=3, verbose_name='Международное сокращение')),
                ('external_code', models.CharField(max_length=4, unique=True, verbose_name='Внешний код')),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
                ('province', models.CharField(max_length=100, verbose_name='Провинция(область)')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('address', models.CharField(max_length=255, unique=True, verbose_name='Адрес')),
                ('external_code', models.CharField(max_length=11, unique=True, verbose_name='Внешний код')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
            },
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.currency', verbose_name='Валюта')),
                ('price_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.pricetype', verbose_name='Тип цены')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='get_settings', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Настройка пользователя',
                'verbose_name_plural': 'Настройки пользователей',
            },
        ),
        migrations.CreateModel(
            name='StockProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.DecimalField(decimal_places=3, max_digits=15, verbose_name='Остаток')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_stock_product', to='shop.product', verbose_name='Товар')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_stock_warehouse', to='shop.warehouse', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Остаток',
                'verbose_name_plural': 'Остатки',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit_measure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.unitmeasure', verbose_name='Единица измерения'),
        ),
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Цена')),
                ('date_update', models.DateTimeField(auto_now_add=True, verbose_name='Дата установки цены')),
                ('discount_percentage', models.DecimalField(decimal_places=0, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка %')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.currency', verbose_name='Валюта')),
                ('price_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.pricetype', verbose_name='Тип цены')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_prices', to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Цена',
                'verbose_name_plural': 'Цены',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionid', models.CharField(blank=True, default='', max_length=40, verbose_name='Ключ сессии')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='Email')),
                ('id_messenger', models.IntegerField(blank=True, default=0, verbose_name='ID из мессенджера')),
                ('address', models.CharField(blank=True, default='', max_length=1024, verbose_name='Адрес доставки')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('delivery_date', models.DateField(default=django.utils.datetime_safe.date.today, verbose_name='Плановая дата доставки')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Комментарий к заказу')),
                ('quantity', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=15, verbose_name='Общее количество')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, verbose_name='Общая сумма')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, verbose_name='Общая скидка')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('canceled', models.BooleanField(default=False, verbose_name='Отменен')),
                ('external_code', models.CharField(blank=True, default='', max_length=11, verbose_name='Внешний номер')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.coupon', verbose_name='Купон')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.currency', verbose_name='Валюта заказа')),
                ('delivery_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.deliverytype', verbose_name='Способ получения')),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.paymenttype', verbose_name='Вид оплаты')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.status', verbose_name='Статус заказа')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_orders', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.warehouse', verbose_name='Склад (магазин) отгрузки')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('-time_create',),
            },
        ),
        migrations.CreateModel(
            name='ImageProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=shop.models.get_path_to_image, verbose_name='Изображение')),
                ('description', models.CharField(max_length=100, verbose_name='Описание')),
                ('default', models.BooleanField(blank=True, default=False, verbose_name='Основное')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_images', to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Изображение товара',
                'verbose_name_plural': 'Изображения товаров',
            },
        ),
        migrations.CreateModel(
            name='FavoriteProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_messenger', models.IntegerField(blank=True, default=0, verbose_name='ID из мессенджера')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Избранный товар',
                'verbose_name_plural': 'Избранные товары',
            },
        ),
        migrations.AddField(
            model_name='coupon',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.currency', verbose_name='Валюта заказа'),
        ),
        migrations.CreateModel(
            name='ContractorUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.contractor', verbose_name='Контрагент')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_contractors', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Контрагент пользователя',
                'verbose_name_plural': 'Контрагенты пользователей',
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_messenger', models.IntegerField(blank=True, default=0, verbose_name='ID из мессенджера')),
                ('phone', models.CharField(blank=True, default='', max_length=15, verbose_name='Телефон')),
                ('quantity', models.DecimalField(decimal_places=3, default=1, max_digits=15, verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Цена')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, verbose_name='Скидка')),
                ('discount_percentage', models.DecimalField(decimal_places=0, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка %')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Сумма')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_cart_products', to='shop.cart', verbose_name='Корзина')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_order_products', to='shop.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.warehouse', verbose_name='Склад (магазин)')),
            ],
            options={
                'verbose_name': 'Строка товара в корзине или заказе',
                'verbose_name_plural': 'Строки товаров в корзинах или заказах',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.currency', verbose_name='Валюта корзины'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_user_cart', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.CreateModel(
            name='AttributeValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string_value', models.CharField(max_length=100, verbose_name='Строковое значение')),
                ('numeric_value', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Числовое значение')),
                ('external_code', models.CharField(max_length=11, unique=True, verbose_name='Внешний код')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_values', to='shop.attribute', verbose_name='Атрибут')),
            ],
            options={
                'verbose_name': 'Значение атрибута',
                'verbose_name_plural': 'Значения атрибута',
            },
        ),
        migrations.CreateModel(
            name='AttributeProductValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.attribute', verbose_name='Атрибут')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_attributes_product', to='shop.product', verbose_name='Товар')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.attributevalues', verbose_name='Значение атрибута')),
            ],
            options={
                'verbose_name': 'Значение атрибута для товара',
                'verbose_name_plural': 'Значения атрибутов для товаров',
            },
        ),
        migrations.AddField(
            model_name='attribute',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_attributes_category', to='shop.category', verbose_name='Категория'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id', 'slug'], name='shop_produc_id_f21274_idx'),
        ),
    ]
