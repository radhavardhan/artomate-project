# Generated by Django 2.2.6 on 2019-12-24 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_auto_20191224_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postproject',
            name='category_id',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='postproject',
            name='files',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
