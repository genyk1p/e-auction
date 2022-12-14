# Generated by Django 3.1.3 on 2020-12-03 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20201203_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=160, verbose_name='Meta Tag Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_de',
            field=models.CharField(blank=True, default=None, max_length=160, null=True, verbose_name='Meta Tag Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_en',
            field=models.CharField(blank=True, default=None, max_length=160, null=True, verbose_name='Meta Tag Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_es',
            field=models.CharField(blank=True, default=None, max_length=160, null=True, verbose_name='Meta Tag Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_fr',
            field=models.CharField(blank=True, default=None, max_length=160, null=True, verbose_name='Meta Tag Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_ru',
            field=models.CharField(blank=True, default=None, max_length=160, null=True, verbose_name='Meta Tag Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(blank=True, max_length=80, verbose_name='Meta Tag Title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_de',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Meta Tag Title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_en',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Meta Tag Title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_es',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Meta Tag Title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_fr',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Meta Tag Title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_ru',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Meta Tag Title'),
        ),
    ]
