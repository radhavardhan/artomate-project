# Generated by Django 2.2.6 on 2020-01-22 12:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0056_auto_20200121_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
