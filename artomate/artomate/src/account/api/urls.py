from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from account.api.views import (
    registration_view,
    login,generate,


)
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from account.api import views, KycView,projectview,skillview,categoryview,bidview,send_otp,userprofileview,ticketview,freelancerview

app_name = 'account'

urlpatterns = [

    path('token',TokenObtainPairView.as_view()),
    path('token/refresh',TokenRefreshView.as_view()),
    path('jwt_test',views.MyTokenObtain.as_view()),
    path('jwt_test/refresh',TokenRefreshView.as_view()),

    path('index',views.TestIndex.as_view()),
    path('register', registration_view, name="register"),
    path('login', login),
    path('logout',views.Logout.as_view()),
    path('dashboard', views.DashboardView.as_view()),

            #OTP
    path('sendotp',views.ValidatePhoneSendOTP.as_view()),
    path('twiliosendotp', send_otp.TWILIOSendOTP.as_view()),
    path('pwd',send_otp.Encrypt.as_view()),
    path('pwd12/<str:txt>',send_otp.Decreypt.as_view()),
    # path('otp',send_otp.SendOtp.as_view()),

            # Kyc View
    path('kyc',KycView.KycView.as_view()),
    path('getkyc',KycView.KycStatusView.as_view()),

            #country and experiance
    path('country',KycView.CountryView.as_view()),
    path('experience',KycView.ExperianceView.as_view()),

                # Projects view
    path('postproject',projectview.Projects.as_view()),
    path('projectlist',projectview.AllProjects.as_view()),
    path('singlejob/<str:projectroute>',projectview.SingleJob.as_view()),
    path('testfunction', projectview.Proj.as_view()),
    path('project_on_category/<str:category_code>', projectview.ProjectOnCategory.as_view()),



    # reverse('projects_on_skills',projectview.ProjectOnSkill1.as_view(), *args),

             # Skill view
    path('skills', skillview.Const_Skill_Add.as_view()),
    path('skill_view', skillview.Skill_view.as_view()),
    path('projects_on_multipleskill/', skillview.ProjectMultipleSkill.as_view()),
    path('users_on_multipleskill/',skillview.UserMultipleSkill.as_view()),
    path('projects_on_skills/<str:skill_code>', skillview.ProjectOnSkill.as_view()),
    path('projects_on_skills2/<str:skill_code1>/<str:skill_code2>', skillview.ProjectOnSkill1.as_view()),
    path('projects_on_skills3', skillview.ProjectOnSkill13.as_view()),
    path('freelancer_on_skills/<str:skill_code>', skillview.UserOnSkill.as_view()),



        # Category and subcategory view
    path('category', categoryview.Category.as_view()),
    path('subcategory', categoryview.SubCategory1.as_view()),
    path('allcategories', categoryview.AllCategories.as_view()),
    path('categorylist/<int:cat_id>', categoryview.CategoryList.as_view()),
    path('jobsoncategory',categoryview.JobsOnCategory.as_view()),


                #ticket

    path('tickettype', ticketview.TicketTypeView.as_view()),
    path('raiseticket', ticketview.Raiseticket.as_view()),
    path('ticketview', ticketview.TicketView.as_view()),

    path('random',generate),

        #budget
    path('budget/<int:budget_id>/<int:currency_id>',views.BudgetsDetails.as_view()),
    path('budgetid/<int:budget_id>',views.BudgetIDDetails.as_view()),

    path('uservalidate', views.UsernameValidation.as_view()),
    path('uservalidation12', views.UsernameValidation123.as_view()),

            # freelancer view
    path('allfreelancer',freelancerview.FreelancerList.as_view()),
    path('freelancer/<str:username>', freelancerview.FreelancerView.as_view()),
    path('searchfreelanceronname',freelancerview.FilterFreelancerList.as_view()),
    path('searchfreelanceronskill',freelancerview.FilterFreelanerOnSkill.as_view()),
    path('users_on_multipleskill/', freelancerview.UsersOnMultiplSkill.as_view()),

    path('filterfreelanceroncountry/<int:country_id>',freelancerview.FilterFreelancerOnCountry.as_view()),
    path('filterfreelanceronlang/<int:lang_id>',freelancerview.FreelancerOnLanguage.as_view()),
    path('recentcreatedfreelancers',freelancerview.RecentlyCreatedUser.as_view()),


            #searchfilter
    path('searchfilter',freelancerview.SearchFilter.as_view()),
    path('filterjobsonexperience/<int:exp_id>', freelancerview.SearchJobOnExperience.as_view()),



            #profileview

    path('updateprofilepic', userprofileview.updateprofilepic.as_view()),
    path('updateuserprofile', userprofileview.updateuserprofile.as_view()),
    path('UserPortfolioProfile', userprofileview.addportfolio.as_view()),
    path('getportfolio', userprofileview.getportfolio.as_view()),
    path('profileview', userprofileview.ProfileVeiw.as_view()),
    path('updateprofile', userprofileview.updateuserprofile.as_view()),
    path('pwdchange', userprofileview.ChangePassword.as_view()),
    path('addlanguage', userprofileview.AddLanguage.as_view()),
    path('languageview', userprofileview.LanguageView.as_view()),



        # bid view
    path('bidproject',bidview.BidRequest.as_view()),
    # path('projectsbidview',bidview.ProjectsBidViews.as_view()),

            # hirer posted job details
    path('hirerprojects',bidview.HirerProjects.as_view()),
            # bid details of each project
    path('biddetailsofproject/<str:projectroute>',bidview.Bid_Details_Project.as_view()),
            #users bid details of each project
    path('usersbiddeatilsproject',bidview.No_Of_Bid.as_view()),


    path('selectbid',bidview.Select_Bid.as_view()),

    path('testjson', views.TestJson.as_view()),

    # url(r'^projects_on_skills/(?P<skill_code>\w+)$', views.ProjectOnSkill1.as_view()),

    # Ticket
    # path('raiseticket',)




]
