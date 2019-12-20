from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.views import APIView
from rest_framework.response import Response
import random
import string
from random import choice
from string import ascii_lowercase, digits, hexdigits
from rest_framework.views import APIView
from account.models import Categories,SubCategory,Const_skills
from account.api.serializers import  CategoriesSerializer,SubCategorySerializer




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
            # Const_skills = Skills.objects.filter(category_id=cat_id).values()
            skills = Const_skills.objects.filter(category_id=cat_id).values('skill_name')
            print(skills)
            mylist=[]
            mylist.append(sub)
            mylist.append(skills)
            data={}
            data['result']=mylist

            return Response(data)
