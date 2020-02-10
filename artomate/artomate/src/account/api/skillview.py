import random
import string

from django.db.models import Q, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Const_skills, Skills, PostProject, Bidproject, User_Skills, Userprofile, KycInfo, country
from account.api.serializers import Const_SkillSerializer
from account.api import projectview
from django.http import HttpResponse, JsonResponse, Http404


class Skill_view(APIView):

    def get(self, request):
        skills = Const_skills.objects.all().values('id', 'skill_name', 'skill_code')
        # print(skills)
        data = {}
        data['skills'] = skills
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


class ProjectOnSkill(APIView):
    def get(self, request, skill_code):

        skill = skill_code
        mylist = []
        data = {}
        data1 = {}
        value = Const_skills.objects.filter(skill_code=skill).values('id')
        if value.exists():

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


class UserOnSkill(APIView):
    def get(self, request, skill_code):

        skill = skill_code
        mylist = []
        data = {}
        data1 = {}
        value = Const_skills.objects.filter(skill_code=skill).values('id')
        if value.exists():

            for i in value:
                value1 = User_Skills.objects.filter(skill_id=i['id']).values('user_id')
                if value1.exists():

                    for j in value1:
                        results = Userprofile.objects.filter(user_id=j['user_id']).values('user_name', 'designation',
                                                                                          'hourely_rate',
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


class ProjectOnSkill1(APIView):
    # print(123445)

    def get(self, request, skill_code1, skill_code2):
        skill1 = skill_code1
        skill2 = skill_code2
        data = {}
        # print(skill_code1,skill_code2)
        value = Skills.objects.filter(Q(skill_id=skill1) | Q(skill_id=skill2)).values('project_id')
        # print(123)

        mylist = []
        for var in value:
            projects = PostProject.objects.filter(id=var['project_id']).values('project_title', 'route', 'project_code')
            # print(projects)
            mylist.append(projects)

        data['projects'] = mylist

        return Response(data)


class ProjectOnSkill13(APIView):

    def post(self, request):
        project_list = []
        project_id=[]
        skills = request.data['skills']
        for i in skills:
            var = Skills.objects.filter(skill_id=i['id']).values('project_id')
            # project_id.append(var)
            # print(project_id)
            for j in var:
                projects = PostProject.objects.filter(id=j['project_id']).values('id','project_title', 'route', 'project_code')
                project_list.append(projects)
        return Response(project_list)


class TestFunctions(APIView):
    def get(self, request):
        foo = projectview.test()
        return JsonResponse(foo, safe=False)


class ProjectMultipleSkill(APIView):

    def get(self, request,skill=None):
        mylist=[]
        mylist2=[]
        res = []
        data={}

        skill_code=request.GET.get('skill')
        skillseparate =skill_code.split('_')
        for i in skillseparate:
            project_id = Skills.objects.filter(skill_name=i).values('project_id')
            mylist2.append(project_id)
            for items in mylist2:
                for var in items:
                    if var not in res:
                        res.append(var)
        # print(res)
        # print("=========================")
        for j in res:
            projectslist = PostProject.objects.filter(id=j['project_id']).values()
            mylist.append(projectslist)
        # print(mylist)

        if len(mylist)==0:
            data['message'] = "Not Found"
            data['status'] = 102
            return Response(data)
        else:
            data['data'] = mylist
            data['total'] = len(mylist)
            data['message'] = "success"
            data['status'] = 100
            return Response(data)


class UserMultipleSkill(APIView):
    pass

