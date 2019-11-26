from django.http import HttpResponse, JsonResponse, Http404
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

import random
import string
from django.conf import settings
from django.db.models import Max, Q, Count

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.utils import json

from account.models import KycInfo, Account, Categories, PostProject, Userprofile, SubCategory, Skills, Budgets, \
    Bidproject, No_of_bids_for_project, Const_skills, Json_data

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

from account.api.serializers import RegistrationSerializer, LoginSerializer, KYCInfoSerializer, CategoriesSerializer, \
    BidProjectSerializer, PostProjectSerializer, UserProfileSerializer, SubCategorySerializer, Const_SkillSerializer, \
    NoOfBidProjectSerializer

from random import choice
from string import ascii_lowercase, digits, hexdigits


@api_view(['POST', ])
def registration_view(request):
    user = request.data['username']

    if user == 'yes':
        string2 = ''.join(choice(digits) for i in range(8))
        string3 = ''.join(choice(ascii_lowercase) for i in range(3))
        randomstring = 'f' + string2 + string3
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
    token, _ = Token.objects.get_or_create(user=user)
    postpro = KycInfo.objects.filter(userid=user.id)
    if postpro.exists():
        for kyc in postpro:
            if kyc.kycstatus == 1:
                return Response({'token': token.key, 'kyc_message': 'kyc details uploaded', 'kyc_status': 1},
                                status=HTTP_200_OK)
            elif kyc.kycstatus == 2:
                return Response({'token': token.key, 'kyc_message': 'kyc details pending', 'kyc_status': 2},
                                status=HTTP_200_OK)
            elif kyc.kycstatus == 3:
                return Response({'token': token.key, 'kyc_message': 'kyc details approved', 'kyc_status': 3},
                                status=HTTP_200_OK)
            else:
                if kyc.kycstatus == 4:
                    return Response({'token': token.key, 'kyc_message': 'kyc details rejected', 'kyc_status': 4},
                                    status=HTTP_200_OK)
    return Response({'token': token.key, 'kyc_message': 'kyc details not entered', 'kyc_status': 0},
                    status=HTTP_200_OK)


class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        name = user.username
        id = user.id
        print(id)
        profile = Userprofile.objects.filter(userid=id).values()
        print(profile)

        data = {
            "username": request.user.username,
            "email": request.user.email
        }
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
            profile.userid = user.id
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
        profile = Userprofile.objects.filter(userid=user_id).values()
        return JsonResponse({"profile": list(profile)})





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


class UsernameValidate(APIView):
    def get(self, request):
        name = request.data['username']
        # print(name)
        usernameval = Account.objects.filter(username=name)
        if usernameval.exists():
            return Response('Username already taken', status=HTTP_404_NOT_FOUND)
        else:
            return Response('Success', status=HTTP_200_OK)





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
