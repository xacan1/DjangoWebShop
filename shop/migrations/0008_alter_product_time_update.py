# Generated by Django 4.0.2 on 2022-02-21 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_order_first_name_alter_order_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Изменен'),
        ),
    ]
