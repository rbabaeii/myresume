# Generated by Django 4.1.7 on 2023-03-23 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_data_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='id',
            field=models.UUIDField(editable=None, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
    ]