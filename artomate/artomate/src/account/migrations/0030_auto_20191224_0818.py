# Generated by Django 2.2.6 on 2019-12-24 08:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0029_auto_20191224_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='postproject',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created_at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postproject',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updates_at'),
        ),
    ]
