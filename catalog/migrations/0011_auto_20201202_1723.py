# Generated by Django 3.1.3 on 2020-12-02 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20201202_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='fifth_label_required',
            field=models.BooleanField(default=False, verbose_name='Fifth label required'),
        ),
        migrations.AddField(
            model_name='product',
            name='first_label_required',
            field=models.BooleanField(default=False, verbose_name='First label required'),
        ),
        migrations.AddField(
            model_name='product',
            name='fourth_label_required',
            field=models.BooleanField(default=False, verbose_name='Fourth label required'),
        ),
        migrations.AddField(
            model_name='product',
            name='second_label_required',
            field=models.BooleanField(default=False, verbose_name='Second label required'),
        ),
        migrations.AddField(
            model_name='product',
            name='third_label_required',
            field=models.BooleanField(default=False, verbose_name='Third label required'),
        ),
    ]
