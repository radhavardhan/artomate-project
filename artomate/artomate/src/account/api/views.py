from django.http import HttpResponse, JsonResponse, Http404
from django.utils.translation import LANGUAGE_SESSION_KEY
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
from rest_framework.permissions import AllowAny, IsAuthenticated
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
from rest_framework_simplejwt.views import TokenObtainPairView

from account.api import serializers
from account.models import KycInfo, Account, Categories, PostProject, Userprofile, SubCategory, Skills, Budgets, \
    Bidproject, No_of_bids_for_project, Const_skills, Json_data, Phone_OTP,User_Skills,country

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
        size=5

        string2 = 'Artomateuser' +''.join(choice(digits) for i in range(5))

        randomstring =  string2
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            account.username = randomstring
            account.is_freelancer = 1
            account.save()
            data['response'] = 'Successfully registered'
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
            account.save()
            data['response'] = 'Successfully registered'
        else:
            data = serializer.errors
        return Response(data)


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
        user = request.user
        name = user.username
        id = user.id
        Biddetails = Bidproject.objects.filter(user_id=id).count()
        totalbid = Bidproject.objects.filter(user_id=id).aggregate(Sum('bid_amount'))
        kyc_status = KycInfo.objects.filter(userid=user.id)
        data = {}
        data['user_name'] = name
        data['email']=request.user.email
        data['no_of_bids'] = Biddetails
        data['Task Bids Won'] = 5
        data['Reviews'] = 2
        data['Completed_jobs'] = 2
        data['Monthly_Earnings'] = totalbid
        if kyc_status.exists():
            for var in kyc_status:
                data['kyc_status'] = var.kycstatus
        else:
                data['kyc_status'] = 0
        return JsonResponse(data)


class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user

        serializer = UserProfileSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            profile = serializer.save()
            profile.name = user.username
            profile.user_id = user.id
            profile.email=user.email
            profile.save()
            data['result'] = 'success'
            data['status'] = 1
        else:
            data['status'] = 0
            data = serializer.errors
        return Response(data)



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

class UpdateProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if request.method=='POST':
            user=request.user
            profile = Userprofile.objects.filter(user_id=user.id).values()
            for var in profile:
                print(var)
        return Response("done")


class updateuserprofile(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        user = request.user
        # user_id = user.id
        userprofile = Userprofile.objects.get(user_id=user.id)
        userprofile.first_name = request.data['first_name']
        userprofile.last_name = request.data['last_name']
        userprofile.email = request.data['email']
        userprofile.hourely_rate = request.data['hourely_rate']
        userprofile.portfolio = request.data['portfolio']
        userprofile.designation = request.data['designation']
        userprofile.description = request.data['description']
        userprofile.save()
        return Response("success")




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


class UsernameValidation(APIView):
    def post(self, request):
        if request.method == 'POST':
            name = request.data['username']

            usernameval = Account.objects.filter(username=name)
            if usernameval.exists():
                return Response('Username already taken', status=HTTP_404_NOT_FOUND)
            else:
                return Response('Success', status=HTTP_200_OK)


class FreelancerView(APIView):
    def get(self, request,userid):
        user = Account.objects.filter(id=userid).values('email','username','date_joined')
        data={}
        data['Freelancer']=user
        return Response(data)

class TestJson(APIView):
    def post(self, request):
        # if 'application/json' in request.META['CONTENT_TYPE']:

        data1 = json.loads(request.body)
        skillname = request.data['skills']
        for i in skillname:
            post = Json_data.objects.create()
            post.skillcode = i['skill_name']
            post.save()
            print(i['skill_name'])
        # myslist=
        #     data
        # for i in data1['skills']:
        #     post = Json_data.objects.create()
        #     post.skillcode = i['skill_name']
        #     post.save()
        #
        #     print(i['skill_id'])
        # print(list(data1))

        id = data1.get('id', None)
        skill_code = data1.get('skill_name', None)
        print(id)
        print(skill_code)

        post = Json_data.objects.create(id=id)

        post.skill_code = skill_code

        return HttpResponse('done')


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



class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user = getattr(request, 'user', None)
        if not getattr(user, 'is_authenticated', True):
            user = None
        user_logged_out.send(sender=user.__class__, request=request, user=user)

        # remember language choice saved to session
        language = request.session.get(LANGUAGE_SESSION_KEY)

        request.session.flush()

        if language is not None:
            request.session[LANGUAGE_SESSION_KEY] = language

        if hasattr(request, 'user'):
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()

        print(user.username)

        return Response('done')
