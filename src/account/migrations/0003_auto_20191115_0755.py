# Generated by Django 2.2.6 on 2019-11-15 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20191115_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='country_phone',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='skills',
            name='category_id',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='sub_category_id',
            field=models.IntegerField(blank=True),
        ),
    ]