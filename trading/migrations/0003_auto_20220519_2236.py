# Generated by Django 3.2.13 on 2022-05-19 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0002_auto_20220519_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
