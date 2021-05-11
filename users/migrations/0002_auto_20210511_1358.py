# Generated by Django 3.2.2 on 2021-05-11 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlist',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderlist',
            name='product_selection',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderList',
        ),
        migrations.DeleteModel(
            name='OrderStatus',
        ),
        migrations.DeleteModel(
            name='PaymentMethod',
        ),
        migrations.DeleteModel(
            name='WishList',
        ),
    ]
