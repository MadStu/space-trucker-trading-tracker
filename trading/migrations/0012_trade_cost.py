# Generated by Django 3.2.13 on 2022-05-23 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0011_rename_cost_trade_profit'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]