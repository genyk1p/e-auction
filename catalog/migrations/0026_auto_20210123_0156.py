# Generated by Django 3.1.3 on 2021-01-22 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_product_option_select_3'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='skype',
            field=models.CharField(blank=True, default=None, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='telegram',
            field=models.CharField(blank=True, default=None, max_length=40, null=True),
        ),
    ]
