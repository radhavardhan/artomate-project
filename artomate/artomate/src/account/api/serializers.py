import datetime


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from jwt.compat import text_type
from requests import Response
import json

from rest_framework import serializers, status

from rest_framework.authtoken.models import Token


from django.utils.six import text_type
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import Account,KycInfo,Categories,PostProject,Userprofile,SubCategory,Skills,Bidproject,No_of_bids_for_project,Const_skills,Hirer_bid_select


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    # mobile = serializers.CharField(min_length=10, max_length=12)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],

        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = ['id', 'name', 'email', 'phone', 'skills', 'profile', 'coverphoto', 'country']

    def save(self):
        profile = Userprofile(
            phone=self.validated_data['phone'],
            email = self.validated_data['email'],
            skills=self.validated_data['skills'],
            profile = self.validated_data['profile'],
            coverphoto = self.validated_data['coverphoto'],
            country = self.validated_data['country']
            )
        return profile

class KYCInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = KycInfo
        fields = ['id', 'fullname', 'dob', 'mobile', 'idprooffront','idproofback','kycstatus', 'userid']

    def save(self):
        kyc = KycInfo(
            fullname=self.validated_data['fullname'],
            dob=self.validated_data['dob'],
            mobile=self.validated_data['mobile'],
            idprooffront = self.validated_data['idprooffront'],
            idproofback=self.validated_data['idproofback'],
        )
        return kyc



class PostProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostProject
        fields = ('id', 'project_title', 'description', 'files', 'userid', 'username', 'project_code', 'category_id','subcategory_id',
                 'custom_budget', 'project_deadline', 'experience_required', 'country_id', 'budgetType_Id', 'currency_id', 'min', 'max',)

        def save(self):
            project = PostProject(
                project_title=self.validated_data['project_title'],
                description=self.validated_data['description'],
                files=self.validated_data['files'],

                currency_id=self.validated_data['currencyid'],
                budgetType_Id=self.validated_data['budgetTypeId'],
                category_id=self.validated_data['category_id'],
                subcategory_id=self.validated_data['subcategory_id'],
                custom_budget=self.validated_data['custombudget'],
                project_deadline=self.validated_data['projectdeadline'],
                experience_required=self.validated_data['experiencerequired'],
                country_id=self.validated_data['country_id'],
                min=self.validated_data['min'],
                max=self.validated_data['max'],
            )
            return project



class NoOfBidProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = No_of_bids_for_project
        fields = ('id','project_code','project_name','no_of_bid')







class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'category_name', 'category_code')

        def save(self):
            categories = Categories(
                category_name=self.validated_data['category_name'],

            )
            return categories

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'sub_category_name', 'sub_category_code','category_id')

        def save(self):
            subcategories = SubCategory(
                sub_category_name=self.validated_data['sub_category_name'],
                category_id = self.validated_data['category_id']
            )
            return subcategories

class Const_SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Const_skills
        fields = ('id', 'skill_code','skill_name','category_id')

        def save(self):
            skills = Const_skills(
                skill_name=self.validated_data['skill_name'],
                category_id=self.validated_data['category_id']

            )
            return skills

class BidProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bidproject
        fields = ('project_code', 'project_name', 'bid_amount', 'user_id', 'email','project_id','completion_time')

        def save(self):
            bids = Bidproject(
                project_code=self.validated_data['project_code'],
                bid_amount=self.validated_data['bid_amount'],
                email=self.validated_data['email'],
                completion_time=self.validated_data['completion_time']
            )
            return bids

class HirerSelectBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hirer_bid_select
        fields=('hirer_email_id', 'project_id', 'project_route', 'freelancer_email_id','message')
        def save(self):
            bidselect=Hirer_bid_select(

                project_id=self.validated_data['project_id'],
                freelancer_email_id=self.validated_data['freelancer_email_id'],
                message=self.validated_data['message']

            )
            return bidselect



USER_LIFETIME = datetime.timedelta(days=30)


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs['email']
        password = attrs['password']
        user = authenticate(username=username, password=password)

        if not user:
            custom={"Error":"Invalid Credentials","status":"0"}
            return custom

        data = super(TokenObtainPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = text_type(refresh)
        if self.user.is_superuser:
            new_token = refresh.access_token
            new_token.set_exp(lifetime=USER_LIFETIME)
            data['access'] = text_type(new_token)
        else:
            data['access'] = text_type(refresh.access_token)
            postpro = KycInfo.objects.filter(userid=self.user.id)
            if postpro.exists():
                for kyc in postpro:
                    if kyc.kycstatus == 1:
                        data['kyc_message'] = 'kyc details uploaded'
                        data['kyc_status'] = 1
                    elif kyc.kycstatus == 2:
                        data['kyc_message'] = 'kyc details pending'
                        data['kyc_status'] = 2
                    elif kyc.kycstatus == 3:
                        data['kyc_message'] = 'kyc details approved'
                        data['kyc_status'] = 3
                    elif kyc.kycstatus == 4:
                         data['kyc_message'] = 'kyc details rejected'
                         data['kyc_status'] = 4
            else:
                data['kyc_message'] = 'kyc details not entered'
                data['kyc_status'] = 0
        data['user details'] = self.user.email
        return data
