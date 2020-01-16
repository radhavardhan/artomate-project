from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
import random
import string
from random import choice
from string import ascii_lowercase, digits, hexdigits
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import (
    PageNumberPagination,LimitOffsetPagination)

from account.api.pagination import PostLimitOffsetPagination,PostPageNumberPagination
from account.models import Account, Userprofile, User_Skills, user_languages, UserPortfolioProfile, country, Currency, KycInfo,Const_skills,const_languages,Skills,PostProject,\
                            Bidproject

from account.api.serializers import PostProjectSerializer
from django.http import HttpResponse, JsonResponse, Http404


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

class FilterFreelanerOnSkill(APIView):


    def post(self,request):
        data1={}
        data={}
        mylist=[]
        print(13456)
        if 'skillname' in request.data:
            print(13456)
            skill_name = request.data['skillname']
            print(skill_name)
            name=skill_name[:3]
            if  not skill_name:
                data['message']="enter skill_name"
                data['status'] = 102
                return Response(data)
            else:
                print("hi")
                value = Const_skills.objects.filter(skill_name=skill_name).values('id')
                print(value)

                if value.exists():

                    for i in value:
                        value1 = User_Skills.objects.filter(skill_id=i['id']).values('user_id')
                        print(value1)
                        if value1.exists():

                            for j in value1:
                                results = Userprofile.objects.filter(user_id=j['user_id']).values('user_name',
                                                                                                  'designation',
                                                                                                  'hourely_rate',
                                                                                                  'description',
                                                                                                  'profile', 'user_id',
                                                                                                  'country_id')
                                print(results)

                                userfullname = KycInfo.objects.filter(userid=j['user_id']).values('fullname')

                                for k in userfullname:

                                    for i in results:
                                        data = {
                                            "fullname": k['fullname'],
                                            "freelancer": i,
                                            "location": country.objects.filter(id=i['country_id']).values(
                                                'country_name'),
                                            "ratings": 4,
                                            "jobscompleted": 2
                                        }

                                        mylist.append(data)
                            data1['data'] = mylist
                            data1['total'] = len(mylist)

                            return Response(data1)
                        else:
                            data = {}
                            data['message'] = "Not Found"
                            data['status'] = 102
                            return Response(data)

                else:
                    data = {}
                    data['message'] = "Not Found"
                    data['status'] = 102
                    return Response(data)

        else:
            data['message'] = "enter skill_name"
            data['status']=102
            return Response(data)

class FilterFreelancerOnCountry(APIView):
    def get(self,request,country_id):

        data1 = {}
        mylist = []
        userprof = Userprofile.objects.filter(country_id=country_id).values('user_name', 'designation', 'hourely_rate',
                                                                         'description', 'profile', 'user_id',
                                                                         'country_id')

        if userprof.exists():
            for j in userprof:
                data = {
                    'name': KycInfo.objects.filter(userid=j['user_id']).values('fullname'),
                    'user_id': j['user_id'],
                    'designation': j['designation'],
                    'hourely_rate': j['hourely_rate'],
                    'profile': j['profile'],
                    'location': country.objects.filter(id=j['country_id']).values('country_name'),
                    'ratings': 3,
                    'jobscompleted': 3,
                    'skills': User_Skills.objects.filter(user_id=j['user_id']).values('skill_name'),
                    'language': user_languages.objects.filter(user_id=j['user_id']).values('language_name'),
                    'portfolio': UserPortfolioProfile.objects.filter(user_id=j['user_id']).values('project_name',
                                                                                                  'project_images',
                                                                                                  'project_description')
                }
                mylist.append(data)
                data1['data'] = mylist
                data1['total']=len(mylist)
                data1['status'] = 100
                data1['message'] = 'success'
            return Response(data1)
        else:
            data = {}
            data['message'] = "Not Found"
            data['status'] = 102
            return Response(data)


class FreelancerOnLanguage(APIView):

    def get(self,request,lang_id):
        data1 = {}
        mylist = []
        userid = user_languages.objects.filter(language_id=lang_id).values('user_id')
        # print(userid)
        for i in userid:
            userprof = Userprofile.objects.filter(user_id=i['user_id']).values('user_name', 'designation', 'hourely_rate',
                                                                         'description', 'profile', 'user_id',
                                                                         'country_id')
            # print(userprof)

            for j in userprof:
                # print("===========================")
                # print(j)
                data = {
                    'name': KycInfo.objects.filter(userid=j['user_id']).values('fullname'),
                    'user_id':j['user_id'],
                    'designation': j['designation'],
                    'hourely_rate': j['hourely_rate'],
                    'profile': j['profile'],
                    'location': country.objects.filter(id=j['country_id']).values('country_name'),
                    'ratings': 3,
                    'jobscompleted': 3,
                    'skills': User_Skills.objects.filter(user_id=j['user_id']).values('skill_name'),
                    'language': user_languages.objects.filter(user_id=j['user_id']).values('language_name'),
                    'portfolio': UserPortfolioProfile.objects.filter(user_id=j['user_id']).values('project_name',
                                                                                                  'project_images',
                                                                                                  'project_description')
                }
            mylist.append(data)
            data1['data'] = mylist
            data1['total'] = len(mylist)
            data1['status'] = 100
            data1['message'] = 'success'
        return Response(data1)


class SearchFilter(APIView):
    def post(self,request):

        skill =request.data['skill']
        id=request.data['search_id']
        search_id=int(id)
        if search_id == 1:
            value = Const_skills.objects.filter(skill_name=skill).values('id')
            if value.exists():
                data1={}
                mylist = []
                for i in value:
                    value1 = Skills.objects.filter(skill_id=i['id']).values('project_id')

                    if value1.exists():

                        for j in value1:
                            results = PostProject.objects.filter(id=j['project_id']).values('id', 'project_title',
                                                                                            'description', 'min', 'max',
                                                                                            'username', 'created_at',
                                                                                            'route')
                            for k in results:
                                project_skill = Skills.objects.filter(project_id=k['id']).values('skill_name')
                                bid = Bidproject.objects.filter(project_id=k['id']).values('no_of_bid').count()
                                bids = bid
                                data = {"projects": k, "skills": project_skill, "bids": bids}
                                mylist.append(data)

                        data1['data'] = mylist
                        data1['totalcount'] = len(mylist)

                        return Response(data1)
                    else:
                        data = {}
                        data['message'] = "Not Found"
                        data['status'] = 102
                        return Response(data)
            else:
                data = {}
                data['message'] = "Not Found"
                data['status'] = 102
                return Response(data)


        elif search_id == 2:
            value = Const_skills.objects.filter(skill_code=skill).values('id')
            if value.exists():

                for i in value:
                    value1 = User_Skills.objects.filter(skill_id=i['id']).values('user_id')
                    if value1.exists():

                        for j in value1:
                            results = Userprofile.objects.filter(user_id=j['user_id']).values('user_name',
                                                                                              'designation',
                                                                                              'hourely_rate',
                                                                                              'description',
                                                                                              'profile', 'user_id',
                                                                                              'country_id')

                            userfullname = KycInfo.objects.filter(userid=j['user_id']).values('fullname')

                            for k in userfullname:

                                for i in results:
                                    data = {
                                        "fullname": k['fullname'],
                                        "freelancer": i,
                                        "location": country.objects.filter(id=i['country_id']).values('country_name'),
                                        "ratings": 4,
                                        "jobscompleted": 2
                                    }

                                    mylist.append(data)
                        data1['data'] = mylist
                        data1['total'] = len(mylist)

                        return Response(data1)
                    else:
                        data = {}
                        data['message'] = "Not Found"
                        data['status'] = 102
                        return Response(data)

            else:
                data = {}
                data['message'] = "Not Found"
                data['status'] = 102
                return Response(data)

            return Response("freelancer")
        else:
            return Response("acts")

