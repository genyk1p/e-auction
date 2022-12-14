# Generated by Django 3.1.3 on 2020-12-05 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20201203_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionSelectPercent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('admin_name', models.CharField(default='', max_length=50, verbose_name='Имя виджета админке формата Product.admin_name_OptionSelectPercent.name')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='required_select_percent',
            field=models.BooleanField(default=False, verbose_name='Обязательная или нет поле select percent'),
        ),
        migrations.CreateModel(
            name='OptionSelectPercentSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('option_select', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.optionselectpercent')),
                ('option_select_element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.optionselectelement')),
            ],
        ),
        migrations.AddField(
            model_name='optionselectpercent',
            name='elements',
            field=models.ManyToManyField(blank=True, related_name='option_check_box_element_percent', through='catalog.OptionSelectPercentSummary', to='catalog.OptionSelectElement'),
        ),
        migrations.AddField(
            model_name='product',
            name='option_select_percent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='catalog.optionselectpercent'),
        ),
    ]
