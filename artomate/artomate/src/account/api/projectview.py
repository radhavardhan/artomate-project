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
from account.models import PostProject, Skills, Bidproject, Const_skills, Experiance, country, Currency, KycInfo
from account.api.serializers import PostProjectSerializer
from django.http import HttpResponse, JsonResponse, Http404

class ProjectViewPagination(PageNumberPagination):
    page_size = 2

class Proj(APIView):
    pagination_class = ProjectViewPagination

    def get(self,request):
        queryset = PostProject.objects.values('id', 'project_title', 'description', 'min', 'max',
                                              'username', 'created_at').order_by('created_at').reverse()
        data = {}
        data['proj']=queryset
        data['message'] = "success"
        data['status'] = 102
        return Response(data)



class AllProjects(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        queryset = PostProject.objects.values('id', 'project_title', 'description', 'min', 'max',
                                               'username','created_at','route').order_by('created_at').reverse()
        data = {}
        data1={}
        if queryset.exists():

            mylist = []
            for i in queryset:
                project_skill = Skills.objects.filter(project_id=i['id']).values('skill_name')
                bid = Bidproject.objects.filter(project_id=i['id']).values('no_of_bid').count()
                bids=bid
                data= {"projects":i, "skills": project_skill, "bids": bids}
                mylist.append(data)
            total=len(mylist)
            data1['all projects']=mylist
            data1['total']=total
            return Response(data1)
        else:
            data['message']="Not Found"
            data['status']=102
            return Response(data)
    #     data = Proj.projects(request)
    #     return Response(data, safe=False)




class SingleJob(AllProjects):

    def get(self, request ,projectroute):
        singlejob=PostProject.objects.filter(route=projectroute)
        data={}
        for var in singlejob:
            skills = Skills.objects.filter(project_id=var.id).values('skill_name','skill_id')
            data['project_name']=var.project_title
            data['projetc_route']=var.route
            data['descreption'] = var.description
            data['username'] = var.username
            data['min'] = var.min
            data['max']=var.max
            data['project_deadline'] = var.project_deadline
            exp = Experiance.objects.filter(id=var.experience_required).values('Exp_name')
            data['experienced_required'] = exp
            countryname=country.objects.filter(id=var.country_id).values('country_name')
            data['country']=countryname
            courrencytype = Currency.objects.filter(id=var.currency_id).values('currency_type')
            data['currency']=courrencytype
            data['skills']=skills
            data['status']=101
        return Response(data)



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
            string2 = '-' + ''.join(choice(digits) for i in range(8))
            project_title1 = project + string2
            postproject1 = PostProject.objects.all()
            serializer = PostProjectSerializer(data=request.data)
            user_kyc = KycInfo.objects.filter(userid=user.id)
            if user_kyc.exists():
                for kyc in user_kyc:
                    if kyc.kycstatus == 1:
                        data['message'] = "You have uploaded kyc details wait for approve"
                        data['status'] = 1
                        return Response(data)
                    elif kyc.kycstatus == 2:
                        data['message'] = "Your kyc is pending"
                        data['status'] = 0
                        return Response(data)
                    elif kyc.kycstatus == 3:
                        if postproject1.exists():
                            for var in postproject1:

                                if var.project_title == string1:
                                    # print("executing this 2")
                                    project_title12 = project_title1
                                    if serializer.is_valid():
                                        pro = serializer.save()
                                        pro.userid = user.id
                                        cat = request.data['category_id']
                                        cat1=json.dumps(cat)
                                        pro.category_id = cat1
                                        pro.project_code = code
                                        pro.username = user.username
                                        pro.route = project_title12
                                        pro.save()
                                        project_id = pro.id
                                        skillname = request.data['skills']
                                        for i in skillname:
                                            post = Skills.objects.create(skill_id=i['id'], project_id=project_id,
                                                                         skill_name=i['name'])
                                            post.save()
                                        data['result'] = 'success'
                                    else:
                                        data = serializer.errors
                                    return Response(data)

                            # print("executing this 3")
                            project_title2 = project
                            # print(project_title2)
                            if serializer.is_valid():
                                pro = serializer.save()
                                pro.userid = user.id
                                cat = request.data['category_id']
                                cat1 = json.dumps(cat)

                                pro.category_id = cat1

                                pro.project_code = code
                                pro.username = user.username
                                pro.route = project_title2
                                pro.save()
                                project_id = pro.id
                                skillname = request.data['skills']
                                for i in skillname:
                                    post = Skills.objects.create(skill_id=i['id'], project_id=project_id,
                                                                 skill_name=i['name'])
                                    post.save()
                                data['result'] = 'success'
                            else:
                                data = serializer.errors
                            return Response(data)

                        else:

                            project_title2 = project
                            if serializer.is_valid():
                                pro = serializer.save()
                                pro.userid = user.id
                                cat = request.data['category_id']
                                cat1 = json.dumps(cat)

                                pro.category_id = cat1

                                pro.project_code = code
                                pro.username = user.username
                                pro.route = project_title2
                                pro.save()

                                project_id = pro.id
                                skillname = request.data['skills']
                                # print(skillname)
                                for i in skillname:
                                    post = Skills.objects.create(skill_id=i['id'], project_id=project_id, skill_name=i['name'])
                                    post.save()
                                data['result'] = 'success'
                            else:
                                data = serializer.errors
                        return Response(data)
                    else:
                        if kyc.kycstatus == 4:
                            data['message'] = "Your kyc have been rejected"
                            data['status'] = 0
                            return Response(data)
            else:
                data['message'] = "kyc details not entered"
                data['status'] = 0
                return Response(data)


def test():
    testmessage="test it"
    return JsonResponse(testmessage , safe=False)

class HirerProjects(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user=request.user
        id=user.id
        projects =PostProject.objects.filter(userid=id).values('id', 'project_title', 'description', 'min', 'max',
                                               'username','created_at','route').order_by('created_at').reverse()
        data={}
        data['projects']=projects
        data['message']='success'
        data['status']=100
        return Response(data)
