# Generated by Django 4.1 on 2022-08-22 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bank_getways',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
