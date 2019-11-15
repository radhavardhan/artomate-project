from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30,blank = True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_freelancer = models.IntegerField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class KycInfo(models.Model):
    userid = models.IntegerField(default=None, null=True)
    fullname = models.CharField(max_length=100)
    dob = models.DateField()
    mobile = models.CharField(max_length=17)
    idprooffront = models.ImageField(upload_to='pictures/')
    idproofback = models.ImageField(upload_to='pictures/')
    kycstatus = models.IntegerField(null=True)
    username = models.CharField(max_length =100,default=None, null=True)

class country(models.Model):
    country_code = models.CharField(max_length=30, unique=True)
    country_name = models.CharField(max_length=100,unique=True)
    country_phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='updates_at', auto_now=True)


class Categories(models.Model):
    category_name = models.CharField(max_length=50)
    category_code = models.CharField(max_length=60,default =None , null=True,unique=True)

class SubCategory(models.Model):
    category_id = models.IntegerField(default = None)
    sub_category_name = models.CharField(max_length=60)
    sub_category_code = models.CharField(max_length=60, default =None , null=True,unique=True)

class Skills(models.Model):
    category_id = models.IntegerField(blank=True)
    sub_category_id = models.IntegerField(blank=True)
    skills = models.CharField(max_length=40)

class Currency(models.Model):
    currency_type = models.CharField(max_length=30)
    currency_symbol = models.CharField(max_length=30)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='updates_at', auto_now=True)


class BudgetType(models.Model):
    budget_type = models.CharField(max_length=50,default = None)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='updates_at', auto_now=True)

class Budgets(models.Model):
    budgettype_id = models.IntegerField()
    currency_id = models.IntegerField()
    min = models.IntegerField(default =None)
    max = models.IntegerField()
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='updates_at', auto_now=True)

class PostProject(models.Model):
    category_id = models.CharField(max_length=60,blank=True)
    subcategory_id = models.CharField(max_length=60,blank=True)
    project_title = models.CharField(max_length=50)
    route = models.CharField(max_length=100,blank =True)
    project_code = models.CharField(max_length = 30, default =None , null=True,unique=True)
    description = models.CharField(max_length=50)
    files = models.FileField(upload_to='pictures/files/',)
    userid = models.IntegerField(default=None, null=True)
    username = models.CharField(max_length=50,default=None, null=True)
    skills = models.TextField(max_length = 300)
    budgetType_Id = models.IntegerField(default=None)
    currency_id = models.IntegerField(default=None)
    min = models.IntegerField(null=True)
    max=models.IntegerField(null=True)
    custom_budget = models.IntegerField()
    project_deadline = models.DateField()
    experience_required =models.CharField(max_length= 100)
    country_id = models.CharField(max_length= 100)


class Userprofile(models.Model):
    name = models.CharField(max_length=30,null=True)
    user_id = models.IntegerField(default=None, null=True)
    email = models.EmailField()
    phone = models.BigIntegerField()
    skills = models.TextField()
    profile = models.ImageField(upload_to='pictures/')
    cover_photo = models.ImageField(upload_to='pictures/')
    country_id = models.CharField(max_length=30)


class Dashboard(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to='pictures/')
    current_ongoing_jobs = models.CharField(max_length=40)
    completed_recent_projects = models.CharField(max_length=40)
    recommended_jobs = models.CharField(max_length=40)
    wallet = models.IntegerField()
    feedback_reviews=models.CharField(max_length=40)

