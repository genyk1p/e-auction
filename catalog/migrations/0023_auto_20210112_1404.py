# Generated by Django 3.1.3 on 2021-01-12 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_auto_20210112_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_system_settings',
            name='projectId',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
