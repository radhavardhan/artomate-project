# Generated by Django 2.2.6 on 2020-01-03 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0035_blacklistedtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidproject',
            name='completion_time',
            field=models.IntegerField(default=None),
        ),
    ]
