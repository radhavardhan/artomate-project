# Generated by Django 2.2.6 on 2019-11-22 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_skills_skill_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postproject',
            name='files',
            field=models.FileField(null=True, upload_to='pictures/files/'),
        ),
    ]
