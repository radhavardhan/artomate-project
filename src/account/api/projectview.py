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
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import PostProject,Skills,Bidproject,Const_skills
from account.api.serializers import  PostProjectSerializer

class AllProjects(APIView):

    def get(self, request):
        queryset = PostProject.objects.values('id', 'project_title', 'description', 'min', 'max', 'project_deadline','username')

        mylist=[]
        queryset_list = list(queryset)

        for i in queryset_list:
            id=i['id']
            # print(id)
            project_skill = Skills.objects.filter(project_id=id).values('skill_name')
            bid = Bidproject.objects.filter(project_id=id).count()
            mylist.append(i)
            mylist.append(project_skill)
            mylist.append(bid)

        # print(mylist)
        return Response(mylist)



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
            # print(project)

            string2 = '-' + ''.join(choice(digits) for i in range(8))
            project_title = project + string2
            postproject1 = PostProject.objects.all()
            serializer = PostProjectSerializer(data=request.data)
            if postproject1.exists():
                for var in postproject1:
                    # print("executing this 1")
                    if var.project_title == string1:
                        # print("executing this 2")
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
                            # print(skillname)
                            for i in skillname:
                                post = Skills.objects.create(skill_id=i['id'], project_id=project_id,
                                                             skill_name=i['name'])
                                post.save()
                            data['result'] = 'success'

                        else:
                            # print("executing this 3")
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
                                # print(skillname)
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
        data = {}
        skill = skill_code
        mylist = []
        value = Const_skills.objects.filter(skill_code=skill).values('id')
        for i in value:
            value1 = Skills.objects.filter(skill_id=i['id']).values('project_id')
            # print(value1)
            for j in value1:
                results = PostProject.objects.filter(id=j['project_id']).values('project_title', 'route')
                # print('==================================')
                mylist.append(results)

                # print(mylist)
                # print('-----------------------------------')
                # print(results)
                data['Result'] = mylist

        return Response(data)

class ProjectOnSkill1(APIView):


        def get(self, request, skill_code1,skill_code2):
            value =[]
            value.append(skill_code1)
            value.append(skill_code2)
            projects_list = []
            for i in value:
                skill_id = Const_skills.objects.filter(skill_code=i).values('id')
                for j in skill_id:
                    project_id = Skills.objects.filter(skill_id=j['id']).values('project_id')
                    for k in project_id:
                        projects = PostProject.objects.filter(id=k['project_id']).values('project_title','route')
                        projects_list.append(projects)
            return Response(projects_list)
