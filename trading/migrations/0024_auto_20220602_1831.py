# Generated by Django 3.2.13 on 2022-06-02 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0023_auto_20220602_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiplist',
            name='manufacturer',
            field=models.CharField(default='DRAKE', max_length=150),
        ),
        migrations.AddField(
            model_name='userprofit',
            name='ship_code',
            field=models.CharField(default='CATERP', max_length=25),
        ),
    ]