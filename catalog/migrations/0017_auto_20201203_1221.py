# Generated by Django 3.1.3 on 2020-12-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20201203_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='admin_name',
            field=models.CharField(max_length=50, verbose_name='Имя продуктак которое будет использовано для отображения в админке '),
        ),
    ]