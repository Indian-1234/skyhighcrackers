# Generated by Django 4.2.3 on 2023-07-26 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireapp', '0013_delivered_delivery_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='content',
            field=models.TextField(default='1box'),
            preserve_default=False,
        ),
    ]
