# Generated by Django 3.1.3 on 2021-01-23 21:22

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0031_auto_20210123_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='label_value_private',
            field=tinymce.models.HTMLField(default='', verbose_name='Значение приватных элементов label продукта'),
        ),
    ]
