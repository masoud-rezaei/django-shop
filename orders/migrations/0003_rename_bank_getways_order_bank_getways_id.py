# Generated by Django 4.1 on 2022-08-22 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_bank_getways'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='bank_getways',
            new_name='bank_getways_id',
        ),
    ]