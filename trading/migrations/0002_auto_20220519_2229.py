# Generated by Django 3.2.13 on 2022-05-19 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('complete', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Buying',
        ),
        migrations.AddField(
            model_name='item',
            name='todolist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.todolist'),
        ),
    ]
