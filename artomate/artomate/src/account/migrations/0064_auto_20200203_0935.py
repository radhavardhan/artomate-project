# Generated by Django 2.2.6 on 2020-02-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0063_bidproject_bid_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidproject',
            name='bid_status',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
