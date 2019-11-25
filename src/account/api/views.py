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
    Bidproject, No_of_bids_for_project, Const_skills,Json_data

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


class KycView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            id = user.id
            postpro = KycInfo.objects.filter(userid=id)
            print(id)
            if postpro.exists():
                for kycstat in postpro:
                    serializer = KYCInfoSerializer(data=request.data)
                    data = {}
                    if kycstat.kycstatus == 1:
                        data['result'] = 'allready entered kyc details'
                        data['status'] = 0
            else:
                serializer = KYCInfoSerializer(data=request.data)
                data = {}
                if serializer.is_valid():
                    kyc = serializer.save()
                    kyc.username = user.username
                    kyc.userid = user.id
                    kyc.kycstatus = 1
                    kyc.save()
                    data['result'] = 'success'
                    data['status'] = 1
                else:
                    data['status'] = 0
                    data = serializer.errors
        return Response(data)


class AllProjects(APIView):
    def get(self, request):
        queryset = PostProject.objects.values('project_title', 'description', 'min', 'max', 'project_deadline',
                                              'skill1')

        # bid = Bidproject.objects.filter(project_id=project_id).count()

        print(queryset)
        data = {}
        return JsonResponse({"All Jobs": list(queryset)})


class Projects(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            data = {}
            size = 3
            code = 'PR' + ''.join(random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
            string1 = request.data['project_title']

            user = request.user
            project = string1.replace(" ", "-")
            print(project)
            string2 = '-' + ''.join(choice(digits) for i in range(8))
            project_title = project + string2
            postproject1 = PostProject.objects.all()
            serializer = PostProjectSerializer(data=request.data)
            if postproject1.exists():
                for var in postproject1:
                    print("executing this 1")
                    if var.project_title == string1:
                        print("executing this 2")
                        project_title1 = project_title
                        if serializer.is_valid():
                            pro = serializer.save()
                            pro.userid = user.id
                            pro.project_code = code
                            pro.username = user.username
                            pro.route = project_title1
                            pro.save()
                            project_id = pro.id

                            skillname = request.data['skills']
                            for i in skillname:
                                post = Skills.objects.create(skill_id=i['id'], project_id=project_id)
                                post.save()
                            data['result'] = 'success'

                        else:
                            print("executing this 3")
                            project_title2 = project_title
                            if serializer.is_valid():
                                pro = serializer.save()
                                pro.userid = user.id
                                pro.project_code = code
                                pro.username = user.username
                                pro.route = project_title2
                                pro.save()
                                project_id = pro.id
                                skillname = request.data['skills']
                                for i in skillname:
                                    post = Skills.objects.create(skill_id=i['id'], project_id=project_id)

                                    post.save()
                                data['result'] = 'success'
                            else:
                                data = serializer.errors
                        return Response(data)
            else:
                print("executing this 4")
                project_title1 = project
                if serializer.is_valid():
                    pro = serializer.save()
                    pro.userid = user.id
                    pro.project_code = code
                    pro.username = user.username
                    pro.route = project_title1
                    pro.save()
                    postproject1 = pro.id
                    # postproject1 = PostProject.objects.get(userid=user.id)
                    project_id = pro.id
                    skillname = request.data['skills']
                    for i in skillname:
                        post = Skills.objects.create(skill_id=i['id'], project_id=project_id)
                        post.save()
                    data['result'] = 'success'
                else:
                    data = serializer.errors
            return Response(data)




@api_view(["GET"])
def generate(size):
    size = 3
    code = 'PR' + ''.join(random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
    return Response(code)


class Category(APIView):
    def post(self, request):
        if request.method == 'POST':
            size = 3
            catcode = 'CAT' + ''.join(random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
            # subcatcode = 'SUBCAT' + ''.join(random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
            serializer = CategoriesSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                category = serializer.save()
                category.category_code = catcode
                category.save()
                data['result'] = 'success'
                data['status'] = 1
            else:
                data['status'] = 0
                data = serializer.errors
            return Response(data)


class AllCategories(APIView):
    def get(self, request):
        allcategories = Categories.objects.all().values()
        data = {}
        data['categpries'] = allcategories
        return Response(data)


class SubCategory1(APIView):
    def post(self, request):
        if request.method == 'POST':
            category_id = request.data['category_id']
            size = 3
            subcatcode = 'SUBCAT' + ''.join(
                random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
            serializer = SubCategorySerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                subcategory = serializer.save()
                subcategory.sub_category_code = subcatcode
                subcategory.category_id = category_id
                subcategory.save()
                data['result'] = 'success'
                data['status'] = 1
            else:
                data['status'] = 0
                data = serializer.errors
            return Response(data)


class Const_Skill_Add(APIView):
    def post(self, request):
        if request.method == 'POST':
            size = 3
            skillcode = 'SKILL' + ''.join(
                random.choice(string.digits + string.ascii_letters[26:]) for _ in range(size))
            serializer = Const_SkillSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                skills = serializer.save()
                skills.skill_code = skillcode
                skills.save()
                data['result'] = 'Skill added successfully'
                data['status'] = 1
            else:
                data['status'] = 0
                data = serializer.errors
            return Response(data)


class CategoryList(APIView):
    def get(self, request, cat_id):
        if request.method == 'GET':
            # categorylk = request.data['category_id']
            category = Categories.objects.get(id=cat_id)
            # print(category)
            cat_id = category.id
            print(cat_id)
            sub = SubCategory.objects.filter(category_id=cat_id).values()
            # subcategory = SubCategory.objects.filter(category_id = cat_id).values()
            skills = Skills.objects.filter(category_id=cat_id).values()
            data = {}
            data['subcategory'] = sub
            data['skills'] = skills
            print(sub)
            return Response(data)


class BudgetsDetails(APIView):
    def get(self, request, budget_id, currency_id):
        if request.method == 'GET':
            budgets = Budgets.objects.get(budgettype_id=budget_id, currency_id=currency_id)
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


class KycVerify(APIView):
    def get(self, request):
        serializer = KYCInfoSerializer()
        data = {}
        Kyc = serializer.save()
        data['result'] = 'success'
        data['status'] = 1
        return Response(data)


class BidRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            id = user.id
            data = {}
            project_code = request.data['project_code']
            project_bid = PostProject.objects.get(project_code=project_code)
            print(project_bid.id)
            bid = Bidproject.objects.filter(project_code=project_code)
            no_of_bid = Bidproject.objects.filter(project_code=project_code).count()
            print(no_of_bid)
            mylist = []
            for var in bid:
                mylist.append(var.user_id)

            if id in mylist:
                data['response'] = 'You have already bid for this project'
                return Response(data)

            else:
                serializer = BidProjectSerializer(data=request.data)
                data = {}
                if serializer.is_valid():
                    bids = serializer.save()
                    bids.project_name = project_bid.project_title
                    bids.project_id = project_bid.id
                    bids.user_id = id
                    bids.no_of_bid = no_of_bid + 1
                    bids.save()

                    data['result'] = 'success'
                    data['status'] = 1
                else:
                    data = serializer.errors
                    data['status'] = 0
                return Response(data)


class No_Of_Bid(APIView):
    def get(self, request):
        project_id = request.data['project_id']
        data = {}
        data['Total number of bids for project'] = Bidproject.objects.filter(project_id=project_id).count()
        data['Project name'] = Bidproject.objects.filter(project_id=project_id).values(
            'project_name')
        return Response(data)


class ProjectOnSkill(APIView):
    def get(self, request, skill_code):
        data={}
        skill = skill_code
        mylist=[]
        value = Const_skills.objects.filter(skill_code=skill).values('id')
        for i in value:
            value1 = Skills.objects.filter(skill_id=i['id']).values('project_id')
            print(value1)
            for j in value1:
                results = PostProject.objects.filter(id=j['project_id']).values('project_title', 'route')
                print('==================================')
                mylist.append(results)
                print(mylist)
                print('-----------------------------------')
                # print(results)
            # data['response'] = results

        return Response(mylist)


class ProjectOnSkill1(APIView):
    def get(self, request, skill1, skill2):
        print('skill', skill1, 'skill1', skill2)
        data = {}

        # projects = PostProject.objects.filter(skills=skill1).values('project_title')
        # print(projects)
        # projects1 = PostProject.objects.filter(skill1=skill2).values('project_title')
        # print(projects1)

        value = PostProject.objects.filter(Q(skills=skill1) | Q(skill1=skill2)).values()

        data['response'] = value

        return JsonResponse({"models_to_return": list(value)})

class TestJson(APIView):
    def post(self,request):
        # if 'application/json' in request.META['CONTENT_TYPE']:

            data1 = json.loads(request.body)
            skillname= request.data['skills']
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

    def get(self,request):
        skills= Const_skills.objects.all().values('id','skill_name','skill_code')
        print(skills)
        data={}
        data['skills']=skills
        return Response(data)
