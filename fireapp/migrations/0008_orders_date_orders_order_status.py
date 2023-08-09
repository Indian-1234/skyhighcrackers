# Generated by Django 4.2.3 on 2023-07-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireapp', '0007_alter_cartitem_product_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='date',
            field=models.DateField(auto_now_add=True, default='2023-06-23'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='order_status',
            field=models.TextField(default='PENDING'),
        ),
    ]