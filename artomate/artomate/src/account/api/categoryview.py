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
from account.models import Categories,SubCategory,Const_skills,PostProject
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

        mylist=[]
        data1={}
        allcategories = Categories.objects.all().values('id','category_name','category_image')
        for i in allcategories:
            projects = PostProject.objects.filter(category_id=i['id']).count()
            data = {"categories": i, "no of posted jobs": projects}
            mylist.append(data)
        data1['data'] = mylist
        data1['total']=len(mylist)
        return Response(data1)


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
            data['result'] = mylist

            return Response(data)

class JobsOnCategory(APIView):

    def get(self,request):
        mylist = []
        data1 = {}
        allcategories = Categories.objects.all().values('id', 'category_name', 'category_image')
        # print(allcategories)
        # projects = PostProject.objects.latest('created_at')
        projects = PostProject.objects.values('category_id','id').distinct()
        # projects23 = PostProject.objects.values('category_id','id','created_at').filter('category_id').latest('created_at')
        # print(projects)
        # cat_id = [1,2,3,4,5,6]
        # for i in cat_id:
        #
        #     projects12 = PostProject.objects.filter(category_id=i).reverse()
        #     mylist.append(projects12)
        #     print(mylist)
        # for i in allcategories:
        #     projects = PostProject.objects.filter(category_id=i['id']).count()
        #     data = {"categories": i, "no of posted jobs": projects}
        #     mylist.append(data)
        # data1['data'] = mylist
        # data1['total'] = len(mylist)

        data1['pr']=projects


        return Response(data1)

