# Generated by Django 2.2.6 on 2019-12-17 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_auto_20191217_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hirer_bid_select',
            name='project_id',
            field=models.IntegerField(unique=True),
        ),
    ]
