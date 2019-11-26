from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from account.api.views import (
    registration_view,
    login,generate,


)

from account.api import views, KycView,projectview,skillview,categoryview,bidview

app_name = 'account'

urlpatterns = [
    path('register', registration_view, name="register"),
    path('login', login),
    path('dashboard', views.DashboardView.as_view()),

            # Kyc View
    path('kyc',KycView.KycView.as_view()),

                # Projects view
    path('postproject',projectview.Projects.as_view()),
    path('home',projectview.AllProjects.as_view()),
    path('projects_on_skills/<str:skill_code>', projectview.ProjectOnSkill.as_view()),
    path('projects_on_skills/<str:*args>', projectview.ProjectOnSkill1.as_view()),

             # Skill view
    path('skills', skillview.Const_Skill_Add.as_view()),
    path('skill_view', skillview.Skill_view.as_view()),

        # Category and subcategory view
    path('category', categoryview.Category.as_view()),
    path('subcategory', categoryview.SubCategory1.as_view()),
    path('allcategories', categoryview.AllCategories.as_view()),
    path('categorylist/<int:cat_id>', categoryview.CategoryList.as_view()),

    path('random',generate),
        #budget
    path('budget/<int:budget_id>/<int:currency_id>',views.BudgetsDetails.as_view()),

    path('uservalidate', views.UsernameValidation.as_view()),
    path('user', views.UsernameValidate.as_view()),
    path('userprofile',views.UserProfile.as_view()),
    path('profileview',views.ProfileVeiw.as_view()),

        # bid view
    path('bidproject',bidview.BidRequest.as_view()),
    path('totalbid',bidview.No_Of_Bid.as_view()),

    path('testjson', views.TestJson.as_view()),

    # url(r'^projects_on_skills/(?P<skill_code>\w+)$', views.ProjectOnSkill1.as_view()),

]
