# Generated by Django 3.1.3 on 2021-03-23 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0040_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_name',
            field=models.CharField(blank=True, default=None, max_length=101, null=True, verbose_name='Product Name'),
        ),
    ]
