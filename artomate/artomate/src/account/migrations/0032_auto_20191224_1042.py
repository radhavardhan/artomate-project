# Generated by Django 2.2.6 on 2019-12-24 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0031_auto_20191224_0829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='country_name',
            new_name='countryname',
        ),
    ]
