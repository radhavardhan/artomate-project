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
    path('skills',views.Const_Skill_Add.as_view()),
    path('budget/<int:budget_id>/<int:currency_id>',views.BudgetsDetails.as_view()),
    path('allcategories',views.AllCategories.as_view()),
    path('categorylist/<int:cat_id>',views.CategoryList.as_view()),
    path('uservalidate', views.UsernameValidation.as_view()),
    path('user', views.UsernameValidate.as_view()),
    path('userprofile',views.UserProfile.as_view()),
    path('profileview',views.ProfileVeiw.as_view()),
    path('bidproject',views.BidRequest.as_view()),
    path('totalbid',views.No_Of_Bid.as_view()),
    path('projects_on_skills/<str:skill_code>',views.ProjectOnSkill.as_view()),
    # path('projects_on_skills/<str:skill_code1>/<str:skill_code2>',views.ProjectOnSkill1.as_view()),
    path('testjson', views.TestJson.as_view()),
    path('skill_view',views.Skill_view.as_view()),
    url(r'^projects_on_skills/(?P<skill_code>\w+)$', views.ProjectOnSkill1.as_view()),

]




