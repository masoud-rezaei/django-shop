# Generated by Django 4.1 on 2022-08-25 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_bank_getways_order_bank_getways_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]