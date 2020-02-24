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
from account.models import PostProject, Skills, Bidproject, Const_skills, Experiance, country, Currency, KycInfo,Categories,Budgets
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
        queryset = PostProject.objects.filter(project_status=0).values('id', 'project_title', 'description', 'min', 'max',
                                               'username','created_at','route','custom_budget','country_id').order_by('created_at').reverse()
        data = {}
        data1={}
        if queryset.exists():

            mylist = []
            for i in queryset:
                project_skill = Skills.objects.filter(project_id=i['id']).values('skill_name')
                bid = Bidproject.objects.filter(project_id=i['id']).values('no_of_bid').count()
                countryname = country.objects.filter(id=i['country_id']).values('country_name')
                data= {"projects":i,"location":countryname,"skills": project_skill, "bids": bid}

                mylist.append(data)
            total=len(mylist)
            data1['data']=mylist
            data1['total']=total
            return Response(data1)
        else:
            data['message']="Not Found"
            data['status']=102
            return Response(data)




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
            data['skills'] = skills
            data['custombudget']=var.custom_budget
            biddeatils = Bidproject.objects.filter(project_id=var.id).values('bid_amount', 'user_id',
                                                                              'completion_time', 'email')
            norofbid = Bidproject.objects.filter(project_id=var.id).count()
            data['no_of_bid'] = norofbid
            data['bid details'] = biddeatils
            data['message']="success"
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
                                        pro.username =kyc.fullname
                                        pro.route = project_title12
                                        if 'custombudget' in request.data:
                                            custum_bud = request.data['custombudget']
                                            if not custum_bud:
                                                budget_id = request.data['budgetType_Id']
                                                budgets = Budgets.objects.get(id=budget_id)
                                                pro.min = budgets.min
                                                pro.max = budgets.max

                                            else:
                                                pro.custom_budget = custum_bud
                                        pro.project_status=0
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
                            project_title2 = project
                            if serializer.is_valid():
                                pro = serializer.save()
                                pro.userid = user.id
                                cat = request.data['category_id']
                                cat1 = json.dumps(cat)

                                pro.category_id = cat1
                                if 'custombudget' in request.data:
                                    custum_bud = request.data['custombudget']
                                    if not custum_bud:
                                        budget_id = request.data['budgetType_Id']
                                        budgets = Budgets.objects.get(id=budget_id)
                                        pro.min = budgets.min
                                        pro.max = budgets.max

                                    else:
                                        pro.custom_budget = custum_bud

                                pro.project_code = code
                                pro.username = kyc.fullname
                                pro.route = project_title2
                                pro.project_status = 0
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
                                pro.username =kyc.fullname
                                pro.username =kyc.fullname
                                pro.route = project_title2
                                pro.project_status = 0

                                if 'custombudget' in request.data:
                                    custum_bud = request.data['custombudget']
                                    if not custum_bud:
                                        budget_id = request.data['budgetType_Id']
                                        budgets = Budgets.objects.get(id=budget_id)
                                        pro.min = budgets.min
                                        pro.max = budgets.max

                                    else:
                                        pro.custom_budget = custum_bud


                                pro.save()

                                project_id = pro.id
                                skillname = request.data['skills']

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


class ProjectOnCategory(APIView):
    def get(self, request, category_code):

        category = category_code
        mylist = []
        data1 = {}
        category = Categories.objects.filter(category_code=category).values('id')
        data = {}
        if not category:
            data['message'] = "not found"
            data['status'] = 102
            return Response(data)
        else:

            for i in category:
                project = PostProject.objects.filter(category_id=i['id']).values('id', 'project_title', 'route',
                                                                                 'project_code', 'username',
                                                                                 'budgetType_Id', 'currency_id', 'min',
                                                                                 'max', 'custom_budget',
                                                                                 'project_deadline')
                if project.exists():
                    for j in project:
                        project_skill = Skills.objects.filter(project_id=j['id']).values('skill_name')
                        bid = Bidproject.objects.filter(project_id=j['id']).values('no_of_bid').count()
                        bids = bid
                        data = {"projects": j, "skills": project_skill, "bids": bids}

                        mylist.append(data)
                    total = len(mylist)
                    data1['data'] = mylist
                    data1['totalcount'] = total
                    return Response(data1)
                else:
                    data = {}
                    data['message'] = "not found"
                    data['status'] = 102
                    return Response(data)
