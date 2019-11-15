# Generated by Django 2.2.6 on 2019-11-15 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='categorycode',
            new_name='category_code',
        ),
        migrations.RenameField(
            model_name='categories',
            old_name='categoryname',
            new_name='category_name',
        ),
        migrations.RenameField(
            model_name='currency',
            old_name='currencysymbol',
            new_name='currency_symbol',
        ),
        migrations.RenameField(
            model_name='currency',
            old_name='currencytype',
            new_name='currency_type',
        ),
        migrations.RenameField(
            model_name='dashboard',
            old_name='profilepic',
            new_name='profile_pic',
        ),
        migrations.RenameField(
            model_name='postproject',
            old_name='budgetTypeId',
            new_name='budgetType_Id',
        ),
        migrations.RenameField(
            model_name='postproject',
            old_name='country',
            new_name='country_id',
        ),
        migrations.RenameField(
            model_name='postproject',
            old_name='currencyid',
            new_name='currency_id',
        ),
        migrations.RenameField(
            model_name='postproject',
            old_name='custombudget',
            new_name='custom_budget',
        ),
        migrations.RenameField(
            model_name='postproject',
            old_name='experiencerequired',
            new_name='experience_required',
        ),
        migrations.RenameField(
            model_name='postproject',
            old_name='projectcode',
            new_name='project_code',
        ),
        migrations.RenameField(
            model_name='postproject',
            old_name='projectdeadline',
            new_name='project_deadline',
        ),
        migrations.RenameField(
            model_name='postproject',
            old_name='projecttitle',
            new_name='project_title',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='subcategorycode',
            new_name='sub_category_code',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='subcategoryname',
            new_name='sub_category_name',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='country',
            new_name='country_id',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='coverphoto',
            new_name='cover_photo',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='userid',
            new_name='user_id',
        ),
        migrations.AddField(
            model_name='skills',
            name='sub_category_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='skills',
            name='category_id',
            field=models.IntegerField(),
        ),
    ]
