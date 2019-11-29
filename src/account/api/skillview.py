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
from account.models import Const_skills
from account.api.serializers import  Const_SkillSerializer

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
