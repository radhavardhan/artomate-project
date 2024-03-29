from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from account.api.views import (
    registration_view,
    login,generate,


)
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from account.api import views, KycView,projectview,skillview,categoryview,bidview,send_otp

app_name = 'account'

urlpatterns = [

    path('token',TokenObtainPairView.as_view()),
    path('token/refresh',TokenRefreshView.as_view()),
    path('jwt_test',views.MyTokenObtain.as_view()),
    path('jwt_test/refresh',TokenRefreshView.as_view()),


    path('register', registration_view, name="register"),
    path('login', login),
    path('logout',views.Logout.as_view()),
    path('dashboard', views.DashboardView.as_view()),

            #OTP
    path('sendotp',views.ValidatePhoneSendOTP.as_view()),
    path('twiliosendotp', send_otp.TWILIOSendOTP.as_view()),
    # path('otp',send_otp.SendOtp.as_view()),

            # Kyc View
    path('kyc',KycView.KycView.as_view()),
    path('getkyc',KycView.KycStatusView.as_view()),

            #country and experiance
    path('country',KycView.CountryView.as_view()),
    path('experience',KycView.ExperianceView.as_view()),

                # Projects view
    path('postproject',projectview.Projects.as_view()),
    path('home',projectview.AllProjects.as_view()),
    path('projects_on_skills/<str:skill_code>', projectview.ProjectOnSkill.as_view()),
    path('projects_on_skills2/<str:skill_code1>/<str:skill_code2>', projectview.ProjectOnSkill1.as_view()),
    # reverse('projects_on_skills',projectview.ProjectOnSkill1.as_view(), *args),

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
    # path('projectsbidview',bidview.ProjectsBidViews.as_view()),
    path('norofbidforproject',bidview.No_Of_Bid.as_view()),
    path('biddetailsofproject/<str:projectcode>',bidview.Bid_Details_Project.as_view()),
    path('selectbid',bidview.Select_Bid.as_view()),

    path('testjson', views.TestJson.as_view()),

    # url(r'^projects_on_skills/(?P<skill_code>\w+)$', views.ProjectOnSkill1.as_view()),


]
