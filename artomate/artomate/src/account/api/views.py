import os
import uuid
from os import mkdir, chdir

from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.utils.translation import LANGUAGE_SESSION_KEY
from requests import request
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator

import random, jwt
import string
from django.conf import settings
from django.db.models import Max, Q, Count, Sum

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.authentication import authenticate
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth import authenticate, user_logged_out
from rest_framework.authtoken.models import Token
from rest_framework.utils import json
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from account.api import serializers
from account.models import KycInfo, Account, Categories, PostProject, Userprofile, SubCategory, Skills, Budgets, \
    Bidproject, No_of_bids_for_project, Const_skills, Json_data, Phone_OTP,User_Skills,country,BlackListedToken,user_languages,UserPortfolioProfile
from rest_framework.views import APIView
from django.core.mail import send_mail
# from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from account.token import account_activation_token
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMessage

from account.api.serializers import RegistrationSerializer, LoginSerializer, \
    UserProfileSerializer, MyTokenObtainSerializer

from random import choice
from string import ascii_lowercase, digits, hexdigits


@api_view(['POST', ])
def registration_view(request):
    user = request.data['username']

    if user == 'yes':
        size = 5

        string2 = '' + ''.join(choice(digits) for i in range(7))

        randomstring =  string2
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            account.username = randomstring
            account.is_freelancer = 1
            account.bid = 5
            account.save()
            # EMAIL VERIFICATION
            # current_site = get_current_site(request)
            # html_content = render_to_string('acc_active_email.html',
            #                                 {'user': account, 'domain': current_site.domain,
            #                                  'uid': urlsafe_base64_encode(force_bytes(account.pk)),
            #                                  'token': account_activation_token.make_token(account),
            #                                  })
            # email = EmailMultiAlternatives('Confirm your Artomate Account')
            # email.attach_alternative(html_content, "text/html")
            # email.to = [request.data['email']]
            # email.send()

            data['response'] = 'successfully registered new user and ' \
                               'Please confirm your email address to complete the registration '
            data['status'] = 100

        else:
            data = serializer.errors
        return Response(data)

    elif user == 'no':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            account.username = ''
            account.is_freelancer = 0
            account.bid = 5
            account.save()
            # # EMAIL VERIFICATION
            # current_site = get_current_site(request)
            # html_content = render_to_string('acc_active_email.html',
            #                                 {'user': account, 'domain': current_site.domain,
            #                                  'uid': urlsafe_base64_encode(force_bytes(account.pk)),
            #                                  'token': account_activation_token.make_token(account),
            #                                  })
            # email = EmailMultiAlternatives('Confirm your Artomate Account')
            # email.attach_alternative(html_content, "text/html")
            # email.to = [request.data['email']]
            # email.send()

            data['response'] = 'successfully registered new user and ' \
                               'Please confirm your email address to complete the registration '
            data['status'] = 100
        else:
            data = serializer.errors
        return Response(data)


# def activate(request, uidb64, token):
#     try:
#         print("this is activate method")
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         account = Account.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         account = None
#     if account is not None and account_activation_token.check_token(account, token):
#         account.is_active = True
#         account.save()
#         return render(request, 'login.html')
#     else:
#         return HttpResponse('Activation link is invalid!')


def jwt_payload_handler(user):
    pass


def jwt_encode_handler(param):
    pass


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_200_OK)

    #
    # return Response({'token': jwt_encode_handler(jwt_payload_handler(user)),
    #                  'username': user.username})
    payload = {
        'password': user.password,
        'email': user.email,
    }
    # token = {'token': jwt.encode(payload, "SECRET_KEY")}
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    print(token)
    token_decode=jwt.decode(token, 'secret', algorithms=['HS256'])
    print(token_decode)

    # token, _ = Token.objects.get_or_create(user=user)
    postpro = KycInfo.objects.filter(userid=user.id)
    if postpro.exists():
        for kyc in postpro:
            if kyc.kycstatus == 1:
                return Response({'token': token, 'kyc_message': 'kyc details uploaded', 'kyc_status': 1},
                                status=HTTP_200_OK)
            elif kyc.kycstatus == 2:
                return Response({'token': token, 'kyc_message': 'kyc details pending', 'kyc_status': 2},
                                status=HTTP_200_OK)
            elif kyc.kycstatus == 3:
                return Response({'token': token, 'kyc_message': 'kyc details approved', 'kyc_status': 3},
                                status=HTTP_200_OK)
            else:
                if kyc.kycstatus == 4:
                    return Response({'token': token, 'kyc_message': 'kyc details rejected', 'kyc_status': 4},
                                    status=HTTP_200_OK)
    return Response({'token': token, 'kyc_message': 'kyc details not entered', 'kyc_status': 0},
                    status=HTTP_200_OK)


class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {}
        user = request.user
        name = user.username
        id = user.id
        totalbid = Bidproject.objects.filter(user_id=id).aggregate(Sum('bid_amount'))
        kyc_status = KycInfo.objects.filter(userid=user.id)
        profilepic = Account.objects.filter(id=id).values('profile')
        for i in profilepic:
            data['profile'] = i['profile']

        data['user_name'] = name
        data['email'] = request.user.email
        for e in Account.objects.filter(id=id).values('bid'):
            data['Bids'] = e['bid']
        data['no_of_bids'] = Bidproject.objects.filter(user_id=id).count()
        data['jobs_posted'] = PostProject.objects.filter(userid=id).count()
        data['Monthly_Earnings'] = totalbid
        if kyc_status.exists():
            for var in kyc_status:
                data['kyc_status'] = var.kycstatus
        else:
            data['kyc_status'] = 0
        return JsonResponse(data)



class ProfileVeiw(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_id = user.id
        data = {}
        profile = Userprofile.objects.filter(user_id=user_id).values()
        for var in profile:
            countryname = country.objects.filter(id=var['country_id']).values('country_name')
            data={
                "first_name":var['first_name'],
                  "last_name":var['last_name'],
                  "email":var['email'],
                    "hourely_rate":var['hourely_rate'],
                "phone":var['phone'],

                  "countryname":countryname,
                  }

        return Response(data)


@api_view(["GET"])
def generate(size):
    size = 3
    code = 'PR' + ''.join(random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
    return Response(code)


class BudgetsDetails(APIView):
    def get(self, request, budget_id, currency_id):
        if request.method == 'GET':
            # print(123)
            budgets = Budgets.objects.get(budgettype_id=budget_id, currency_id=currency_id)
            # print(budgets)
            data = {}
            data['min'] = budgets.min
            data['max'] = budgets.max
            return Response(data)

class BudgetIDDetails(APIView):
    def get(self, request, budget_id):
        if request.method == 'GET':
            # print(123)
            mylist=[]
            budgets = Budgets.objects.filter(budgettype_id=budget_id).values()
            # print(budgets)
            for i in budgets:
                data={"min":i['min'],"max":i['max']}
                mylist.append(data)

            data1 = {}
            data1['budgets'] = mylist
            data1['total'] = len(mylist)
            data1['message']="success"
            data1['status']=100
            return Response(data1)



class UsernameValidation(APIView):
    permission_classes  =(IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            name = request.data['username']
            data={}

            usernameval = Account.objects.filter(username=name)
            if usernameval.exists():
                data['message']="Username already taken"
                data['status']=1
                return Response(data)
            else:
                return Response('', status=HTTP_200_OK)



class UsernameValidation123(APIView):
    permission_classes  =(IsAuthenticated,)

    def get(self, request):
        try:
            if request.method == 'GET':
                name = request.data['username']
                data={}

                usernameval = Account.objects.filter(username=name)
                if usernameval.exists():
                    data['message']="Username already taken"
                    data['status']=1
                    return Response(data)
                else:
                    return Response('', status=HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class FreelancerView(APIView):
    def get(self, request,username):
        user = Account.objects.filter(username=username).values('email','date_joined')
        data = {}
        data1={}
        mylist=[]
        userprof = Userprofile.objects.filter(user_name=username).values('user_name', 'designation', 'hourely_rate','description','profile','user_id','country_id')
        if userprof.exists():
            for i in user:

                for j in userprof:
                    data={
                        'name':KycInfo.objects.filter(userid=j['user_id']).values('fullname'),
                        'designation':j['designation'],
                        'hourely_rate':j['hourely_rate'],
                        'profile':j['profile'],
                        'location':country.objects.filter(id=j['country_id']).values('country_name'),
                        'ratings':3,
                        'jobscompleted':3,
                        'skills':User_Skills.objects.filter(user_id=j['user_id']).values('skill_name'),
                        'language':user_languages.objects.filter(user_id=j['user_id']).values('language_name'),
                        'portfolio':UserPortfolioProfile.objects.filter(user_id=j['user_id']).values('project_name','project_images','project_description')
                    }
                    mylist.append(data)
                    data1['data']=mylist
                    data1['status']=100
                    data1['message']='success'
            return Response(data1)
        else:
            data = {}
            data['message'] = "Not Found"
            data['status'] = 102
            return Response(data)

class FilterFreelancerList(APIView):
        def post(self,request):
            data1={}
            data={}
            if 'fullname' in request.data:
                full_name =request.data['fullname']
                name=full_name[:3]
                if  not full_name:
                    data['message']="enter fullname"
                    return Response(data)
                else:
                    userdetails = KycInfo.objects.filter(fullname__startswith=name).values('fullname', 'userid')
                    if userdetails.exists():
                        mylist = []
                        list=userdetails
                        for i in list:
                            id=i['userid']

                            user = Userprofile.objects.filter(user_id=id).values('user_name', 'designation', 'hourely_rate', 'description',
                                                                    'profile', 'user_id', 'country_id')

                            for j in user:
                                data = {
                                    "fullname": i['fullname'],
                                    "freelancer": j,
                                    "location": country.objects.filter(id=j['country_id']).values('country_name'),
                                    "ratings": 4,
                                    "jobscompleted": 2
                                }
                                mylist.append(data)
                        data1['data']=mylist
                        data1['total']=len(mylist)

                        return Response(data1)
                    else:
                        data['message']="Not Found"
                        data['status']=102
                        return Response(data)

            else:
                data['message'] = "enter fullname"
                return Response(data)




class FreelancerList(APIView):
        def get(self, request):
            user = Userprofile.objects.all().values('user_name', 'designation', 'hourely_rate', 'description',
                                                    'profile', 'user_id','country_id')
            if user.exists():
                mylist = []
                for i in user:

                    data = {
                        "fullname":KycInfo.objects.filter(userid=i['user_id']).values('fullname'),
                        "freelancer": i,
                        "location": country.objects.filter(id=i['country_id']).values('country_name'),
                        "ratings": 4,
                        "jobscompleted": 2
                    }
                    mylist.append(data)
                return Response(mylist)
            else:
                data = {}
                data['message'] = "Not Found"
                data['status'] = 102
                return Response(data)





class Skill_view(APIView):

    def get(self, request):
        skills = Const_skills.objects.all().values('id', 'skill_name', 'skill_code')
        print(skills)
        data = {}
        data['skills'] = skills
        return Response(data)


class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data['phone']
        if phone_number:
            phone1 = str(phone_number)
            user = Account.objects.filter(phone=phone1)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': "phone number allready exists"
                })
            else:
                print('hi')
                key = self.send_otp(phone_number)
                if key:
                    old = Phone_OTP.objects.filter(phone=phone_number)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'status': False,
                                'datail': 'sending otp error ,limit exceeded'
                            })
                        old.count = count + 1
                        old.save()
                        print("count increase", count)
                        return Response({
                            'sataus': True,
                            'detail': 'OTP sent successfully'
                        })
                    else:
                        print('key genareated')
                        Phone_OTP.objects.create(
                            phone=phone_number,
                            otp=key,
                        )
                        return Response({
                            'status': True,
                            'detail': 'otp sent seccessfully'
                        })
                else:
                    return ({
                        'status': False,
                        'detail': 'sending otp error'
                    })



        else:
            return Response({
                'status': False,
                'detail': "phone number not given"
            })

    def send_otp(self, phone_number):
        print('send otp method')
        if phone_number:

            key = random.randint(999, 9999)
            return key
        else:
            return False


class MyTokenObtain(TokenObtainPairView):

        serializer_class = MyTokenObtainSerializer



class Logout1(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        user=request.user
        print(user.id)
        userdetails = Account.objects.filter(id=user.id).values('is_active')
        userdetails.update(is_active=0)

        return Response("user logged out")


class JSONWebTokenAuthentication(object):
    pass


class Logout(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user =request.user
        user.jwt_secret=uuid.uuid4()
        user.save()

        return Response(status=status.HTTP_200_OK)

class TestIndex(APIView):
    def get(self,request):
        return render(request, 'account/notification.html')

