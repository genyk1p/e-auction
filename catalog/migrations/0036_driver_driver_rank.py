# Generated by Django 3.1.3 on 2021-01-24 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0035_auto_20210124_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='driver_rank',
            field=models.CharField(choices=[('New', 'New'), ('Verified', 'Verified')], default='New', max_length=40),
        ),
    ]
