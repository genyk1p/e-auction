# Generated by Django 3.1.3 on 2020-11-21 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='notification_class',
            field=models.CharField(choices=[('notification is-primary', 'notification is-primary'), ('notification is-link', 'notification is-link'), ('notification is-info', 'notification is-info'), ('notification is-success', 'notification is-success'), ('notification is-warning', 'notification is-warning'), ('notification is-danger', 'notification is-danger')], default='notification is-primary', max_length=23),
        ),
        migrations.AlterField(
            model_name='information',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
