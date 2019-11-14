# Generated by Django 2.2.6 on 2019-11-05 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(max_length=50)),
                ('categorycode', models.CharField(default=None, max_length=60, null=True, unique=True)),
                ('subcategoryname', models.CharField(max_length=60)),
                ('subcategorycode', models.CharField(default=None, max_length=60, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='KycInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(default=None, null=True)),
                ('fullname', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('mobile', models.CharField(max_length=17)),
                ('idprooffront', models.ImageField(upload_to='pictures/')),
                ('idproofback', models.ImageField(upload_to='pictures/')),
                ('kycstatus', models.IntegerField(null=True)),
                ('username', models.CharField(default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=50)),
                ('projectcode', models.CharField(default=None, max_length=30, null=True, unique=True)),
                ('description', models.CharField(max_length=50)),
                ('files', models.FileField(upload_to='pictures/files/')),
                ('userid', models.IntegerField(default=None, null=True)),
                ('username', models.CharField(default=None, max_length=50, null=True)),
                ('skills', models.TextField(max_length=300)),
                ('budgetType', models.CharField(max_length=100)),
                ('currency', models.CharField(max_length=100)),
                ('projectbudget', models.CharField(max_length=100)),
                ('custombudget', models.IntegerField()),
                ('projectdeadline', models.DateField()),
                ('experiencerequired', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
    ]
