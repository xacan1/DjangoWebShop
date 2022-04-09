# Generated by Django 4.0.2 on 2022-02-21 00:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='get_user_cart', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
    ]
