# Generated by Django 2.2.6 on 2019-11-15 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20191115_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='country_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]