# Generated by Django 2.2.6 on 2019-11-25 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_remove_skills_skill_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='skills',
            name='skill_name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
