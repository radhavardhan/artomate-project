# Generated by Django 2.2.6 on 2020-01-07 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0040_account_bid'),
    ]

    operations = [
        migrations.CreateModel(
            name='const_languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='user_languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(max_length=300)),
                ('language_id', models.IntegerField(default=None)),
                ('user_id', models.IntegerField(default=None)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='updates_at')),
            ],
        ),
        migrations.CreateModel(
            name='UserPortfolioProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=None)),
                ('project_name', models.CharField(max_length=300)),
                ('project_images', models.ImageField(upload_to='')),
                ('project_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='updates_at')),
            ],
        ),
    ]
