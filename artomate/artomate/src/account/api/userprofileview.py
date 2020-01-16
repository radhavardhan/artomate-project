from django.contrib.auth.hashers import make_password


from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Userprofile,user_languages, User_Skills,Account,country,const_languages,test_languages,KycInfo
from account.api.serializers import UserProfileSerializer,UserPortfolioProfile,User_portfolioSerializer,LanguageSerializer

class adduserprofile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        if request.method == 'POST':
            print(123)
            user = request.user
            user_id = user.id
            print(user)
            data = {}
            userprofileid = Userprofile.objects.all()
            if userprofileid.exists():
                for i in userprofileid:
                    print(userprofileid)
                    if i.user_id == user_id:
                        data['message'] = "already added your profile details"
                        data['status'] = 102
                        return Response(data)

                    else:
                        language = request.data['language_spoken']
                        skill_name = request.data['userskills']
                        serializer = UserProfileSerializer(data=request.data)

                        if serializer.is_valid():
                            userprofile = serializer.save()
                            userprofile.user_id = user_id
                            userprofile.user_name = user.username
                            for j in language:
                                lang = user_languages.objects.create(user_id=user_id, language_name=j['name'],
                                                                     language_id=j['id'])
                                lang.save()
                            for i in skill_name:
                                post = User_Skills.objects.create(user_id=user_id, skill_name=i['skill_name'],
                                                                  skill_id=i['skill_id'])
                                post.save()

                            userprofile.save()
                            data['result'] = 'success'
                            data['status'] = 101
                            return Response(data)
                        else:
                            data['status'] = 0
                            data = serializer.errors
                            return Response(data)
            else:
                language = request.data['language_spoken']
                skill_name = request.data['userskills']
                serializer = UserProfileSerializer(data=request.data)
                if serializer.is_valid():
                    userprofile = serializer.save()
                    userprofile.user_id = user_id
                    userprofile.user_name = user.username
                    for j in language:
                        lang = user_languages.objects.create(user_id=user_id, language_name=j['name'],
                                                             language_id=j['id'])
                        lang.save()
                    for i in skill_name:
                        post = User_Skills.objects.create(user_id=user_id, skill_name=i['skill_name'],
                                                          skill_id=i['skill_id'])
                        post.save()

                    userprofile.save()
                    data['result'] = 'success'
                    data['status'] = 101
                    return Response(data)
                else:
                    data['status'] = 0
                    data = serializer.errors
                    return Response(data)


class updateuserprofile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            user_id = user.id
            data = {}
            kyc=KycInfo.objects.filter(userid=user_id)
            if kyc.exists():

                if 'user_name' in request.data:
                    name = request.data['user_name']
                    name1 =name.replace(" ","")

                    if not name:
                        data['message'] = "enter user name"
                        data['status'] = 102
                        return Response(data)
                    else:
                        usernameval = Account.objects.filter(username=name1).values('id')
                        for i in usernameval:
                            j=i['id']
                        if j == user_id:
                            userupdate = Userprofile.objects.filter(user_id=user_id)
                            if userupdate.exists():
                                print(1243)
                                userprofile12 = Account.objects.get(id=user_id)
                                userkyc = KycInfo.objects.get(userid=user_id)
                                userkyc.username = name1
                                userkyc.save()
                                userprofile11 = Userprofile.objects.get(user_id=user_id)

                                userprofile11.user_name = name1
                                userprofile12.username = name1
                                userprofile11.about_me = request.data['about_me']
                                userprofile11.hourely_rate = request.data['hourely_rate']
                                userprofile11.designation = request.data['designation']
                                userprofile11.description = request.data['description']
                                userprofile11.company_name = request.data['company_name']
                                userprofile11.phone = request.data['phone']
                                userprofile11.country_id = request.data['country_id']
                                userprofile11.save()
                                userprofile12.save()
                                language = request.data['language_spoken']
                                skill_name = request.data['userskills']
                                data = {}
                                userlang = user_languages.objects.filter(user_id=user_id)
                                userlang.delete()
                                userskills = User_Skills.objects.filter(user_id=user_id)
                                userskills.delete()
                                for j in language:
                                    lang = user_languages.objects.create(user_id=user_id,
                                                                         language_name=j['language_name'],
                                                                         language_id=j['id'])
                                    lang.save()
                                for i in skill_name:
                                    post = User_Skills.objects.create(user_id=user_id, skill_name=i['name'],
                                                                      skill_id=i['id'])
                                    post.save()
                                data['message'] = "success"
                                data['status'] = 100
                                return Response(data)
                            else:
                                user = request.user
                                user_id = user.id
                                data = {}
                                language = request.data['language_spoken']
                                skill_name = request.data['userskills']
                                userprofile12 = Account.objects.get(id=user_id)
                                userprofile12.username = name1
                                userprofile12.save()
                                userkyc = KycInfo.objects.get(userid=user_id)
                                userkyc.username = name1
                                userkyc.save()
                                serializer = UserProfileSerializer(data=request.data)

                                if serializer.is_valid():
                                    userprofile = serializer.save()
                                    userprofile.user_id = user_id
                                    userprofile.user_name = name1
                                    for j in language:
                                        lang = user_languages.objects.create(user_id=user_id,
                                                                             language_name=j['language_name'],
                                                                             language_id=j['id'])
                                        lang.save()
                                    for i in skill_name:
                                        post = User_Skills.objects.create(user_id=user_id, skill_name=i['name'],
                                                                          skill_id=i['id'])
                                        post.save()

                                    userprofile.save()
                                    data['result'] = 'success'
                                    data['status'] = 101
                                    return Response(data)
                                else:
                                    print(7)
                                    data['status'] = 0
                                    data = serializer.errors
                                    return Response(data)
                        else:
                            data['message'] = "Username already exists"
                            data['status'] = 102
                            return Response(data)


                else:
                    userupdate = Userprofile.objects.filter(user_id=user_id)
                    if userupdate.exists():
                        print(1243)
                        userprofile11 = Userprofile.objects.get(user_id=user_id)
                        userprofile11.user_name = user.username
                        userprofile11.about_me = request.data['about_me']
                        userprofile11.hourely_rate = request.data['hourely_rate']
                        userprofile11.designation = request.data['designation']
                        userprofile11.description = request.data['description']
                        userprofile11.company_name = request.data['company_name']
                        userprofile11.phone = request.data['phone']
                        userprofile11.country_id = request.data['country_id']
                        userprofile11.save()

                        language = request.data['language_spoken']
                        skill_name = request.data['userskills']
                        data = {}
                        userlang = user_languages.objects.filter(user_id=user_id)
                        userlang.delete()
                        userskills = User_Skills.objects.filter(user_id=user_id)
                        userskills.delete()
                        for j in language:
                            lang = user_languages.objects.create(user_id=user_id, language_name=j['language_name'],
                                                                 language_id=j['id'])
                            lang.save()
                        for i in skill_name:
                            post = User_Skills.objects.create(user_id=user_id, skill_name=i['name'],
                                                              skill_id=i['id'])
                            post.save()
                        data['message'] = "success"
                        data['status'] = 100
                        return Response(data)
                    else:
                        user = request.user
                        user_id = user.id
                        data = {}
                        language = request.data['language_spoken']
                        skill_name = request.data['userskills']
                        serializer = UserProfileSerializer(data=request.data)
                        if serializer.is_valid():
                            userprofile = serializer.save()
                            userprofile.user_id = user_id
                            userprofile.user_name = user.username
                            for j in language:
                                lang = user_languages.objects.create(user_id=user_id, language_name=j['language_name'],
                                                                     language_id=j['id'])
                                lang.save()
                            for i in skill_name:
                                post = User_Skills.objects.create(user_id=user_id, skill_name=i['name'],
                                                                  skill_id=i['id'])
                                post.save()

                            userprofile.save()
                            data['result'] = 'success'
                            data['status'] = 101
                            return Response(data)
                        else:
                            print(7)
                            data['status'] = 102
                            data = serializer.errors
                            return Response(data)
            else:
                data['message']="please complete kyc and proceed"
                data['status']=103
                return Response(data)


class updateprofilepic(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        user_id = user.id
        data = {}
        kyc = KycInfo.objects.filter(userid=user_id)
        if kyc.exists():
            if 'profile' in request.data:
                photo = request.data['profile']

                print(photo)
                if not photo:
                    data['error'] = "select an image"
                    data['status']=102
                    return Response(data)
                else:
                    userprofilepic = Userprofile.objects.get(user_id=user_id)
                    userprofilepic.profile = request.data['profile']
                    userprofilepic.save()
                    data['message'] = "success"
                    data['status'] = 100
                    return Response(data)
            else:
                data['error'] = "profile required"
                data['status'] = 102
                return Response(data)
        else:
            data['message'] = "please complete kyc and proceed"
            data['status'] = 103
            return Response(data)



class addportfolio(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            userid = user.id
            data = {}
            # file=request.FILES.get['project_images']
            # print(file)
            # print(request.data.project_images)
            serializer = User_portfolioSerializer(data=request.data.project_images)
            if serializer.is_valid():
                portfolio = serializer.save()
                portfolio.user_id = userid
                portfolio.save()
                data['message'] = "success"
                data['status'] = 100
            else:
                data['status'] = 0
                data = serializer.errors
            return Response(data)


class getportfolio(APIView, ):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == 'GET':
            user = request.user
            portfolio = UserPortfolioProfile.objects.filter(user_id=user.id).values('project_name',
                                                                                    'project_description',
                                                                                    'project_images')
            data = {}

            data['project details'] = portfolio

            return Response(data)


class ProfileVeiw(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_id = user.id
        data = {}
        profile = Userprofile.objects.filter(user_id=user_id).values()
        for var in profile:
            countryname = country.objects.filter(id=var['country_id']).values('country_name')
            data = {
                 "first_name":var['first_name'],
                 "last_name":var['last_name'],
                 "email":var['email'],
                 "hourely_rate":var['hourely_rate'],
                 "phone":var['phone'],
                 "countryname":countryname,
                  }

        return Response(data)

class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        user=request.user
        oldpwd = user.password
        pwd1=  request.data['password']
        newpwd=make_password(request.data['password'])
        confirmpwd=request.data['confirmpwd']
        data={}
        if pwd1 != confirmpwd:
            data['message']='password : Passwords must match.'
            data['sataus']=105
        else:
            userpwd=Account.objects.filter(id=user.id).values()
            for i in userpwd:
                i['password']=newpwd
                userpwd.update(password=i['password'])
            data['message']='success'
            data['status']=100
        return Response(data)


class LanguageView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        lang =  const_languages.objects.all().values()
        data={}
        data['languages']=lang
        data['message']="success"
        data['status']=101
        return Response(data)

class AddLanguage(APIView):
    def post(self,request):
        if request.method == 'POST':


            data = {}
            # data1 =  request.data
            # print(data1)
            # text = json.loads(request.data)
            # print(text)
            lang = test_languages.objects.create(language_name={'smelliness': 3, 'crumbliness': 10})
            lang.save()
            # serializer = LanguageSerializer(data=request.data)
            # if serializer.is_valid():
            #     lang = serializer.save()
            #     data['message']=lang
            #     data['result'] = 'success'
            #     data['status'] = 1
            # else:
            #     data['status'] = 0
            #     data = serializer.errors
            return Response("done")


