# Generated by Django 3.2.13 on 2022-06-05 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0026_userprofit_commodity_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofit',
            name='commodity_code',
            field=models.CharField(default='Titanium', max_length=150),
        ),
    ]
