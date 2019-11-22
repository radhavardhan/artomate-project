from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db.models import Max
from rest_framework.authtoken.models import Token
from account.models import Account,KycInfo,Categories,PostProject,Userprofile,SubCategory,Skills,Bidproject,No_of_bids_for_project


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


        # def no_of_Bid(self):
        #     bid = No_of_bids_for_project.objects.filter(project=self)
        #     count_of_bid = bid.aggregate(Max('no_of_bid'))
        #     noofbid = NoOfBidProjectSerializer
        #     noofbid.project_code = bid.project_code
        #     noofbid.project_name = bid.project_name
        #     noofbid.no_of_bid = count_of_bid
        #     noofbid.save()
        #     return noofbid

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

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ('id', 'skills','category_id')

        def save(self):
            skills = Skills(
                skills=self.validated_data['skills'],
                category_id=self.validated_data['category_id']

            )
            return skills

class BidProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bidproject
        fields = ('project_code', 'project_name', 'bid_amount', 'user_id', 'email','project_id')

        def save(self):
            bids = Bidproject(
                project_code=self.validated_data['project_code'],
                bid_amount=self.validated_data['bid_amount'],
                email=self.validated_data['email'],
            )
            return bids

