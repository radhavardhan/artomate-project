from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from account.api.views import (
    registration_view,
    login,generate,


)
from account.api import views

app_name = 'account'

urlpatterns = [
    path('register', registration_view, name="register"),
    path('login', login),
    path('dashboard', views.DashboardView.as_view()),
    path('kyc',views.KycView.as_view()),
    path('postproject',views.Projects.as_view()),
    path('home',views.AllProjects.as_view()),
    path('random',generate),
    path('category',views.Category.as_view()),
    path('subcategory',views.SubCategory1.as_view()),
    path('skills',views.SkillsView.as_view()),
    path('allcategories',views.AllCategories.as_view()),
    path('categorylist/<int:cat_id>',views.CategoryList.as_view()),
    path('uservalidate', views.UsernameValidation.as_view()),
    path('user', views.UsernameValidate.as_view()),
    path('userprofile',views.UserProfile.as_view()),
    path('profileview',views.ProfileVeiw.as_view()),

]




