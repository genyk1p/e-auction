# Generated by Django 3.1.3 on 2020-12-02 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20201202_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='review',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='catalog.review', verbose_name='Review'),
        ),
    ]
