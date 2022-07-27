# Generated by Django 3.1.3 on 2020-12-14 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_auto_20201205_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_de',
            field=models.CharField(max_length=100, null=True, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_en',
            field=models.CharField(max_length=100, null=True, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_es',
            field=models.CharField(max_length=100, null=True, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_fr',
            field=models.CharField(max_length=100, null=True, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Product Name'),
        ),
    ]
