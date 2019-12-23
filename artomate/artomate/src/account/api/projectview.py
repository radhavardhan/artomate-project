from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
import random
import string
from random import choice
from string import ascii_lowercase, digits, hexdigits

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import PostProject, Skills, Bidproject, Const_skills,Experiance,country,Currency
from account.api.serializers import PostProjectSerializer


class AllProjects(APIView):

    def get(self, request):
        queryset = PostProject.objects.values('id', 'project_title', 'description', 'min', 'max',
                                               'username')
        data={}
        mylist = []
        for i in queryset:
            project_skill = Skills.objects.filter(project_id=i['id']).values('skill_name')
            bid = Bidproject.objects.filter(project_id=i['id']).values('no_of_bid').count()
            bids=bid
            data= {"projects":i, "skills": project_skill, "bids": bids}
            mylist.append(data)

        return Response(mylist)



class SingleJob(AllProjects):

    def get(self, request ,projectid):
        singlejob=PostProject.objects.filter(id=projectid)
        data={}
        for var in singlejob:
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
            if postproject1.exists():
                for var in postproject1:
                    # print("executing this 1")
                    if var.project_title == string1:
                        # print("executing this 2")
                        project_title12 = project_title1
                        if serializer.is_valid():
                            pro = serializer.save()
                            pro.userid = user.id
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
                # print("executing this 4")
                project_title2 = project
                if serializer.is_valid():
                    pro = serializer.save()
                    pro.userid = user.id
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


class ProjectOnSkill(APIView):
    def get(self, request, skill_code):

        skill = skill_code
        mylist = []
        value = Const_skills.objects.filter(skill_code=skill).values('id')
        for i in value:
            value1 = Skills.objects.filter(skill_id=i['id']).values('project_id')
            for j in value1:
                results = PostProject.objects.filter(id=j['project_id']).values('project_title', 'route')
                mylist.append(results)

        return Response(mylist)


class ProjectOnSkill1(APIView):
    # print(123445)

    def get(self, request,skill_code1, skill_code2):
        skill1=skill_code1
        skill2=skill_code2
        # projects = Skills.objects.filter(skills=skill1).values('project_title')
        # print(projects)
        # projects1 = PostProject.objects.filter(skill1=skill2).values('project_title')
        # print(projects1)
        data={}

        value = Skills.objects.filter(Q(skill_id=skill1) | Q(skill_id=skill2)).values('project_id')

        mylist=[]
        for var in value:
            projects = PostProject.objects.filter(id=var['project_id']).values('project_title','route','project_code')
            print(projects)
            mylist.append(projects)

        data['projects'] = mylist

        return Response(data)
