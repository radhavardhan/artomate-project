from django.db.models import Sum
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import PostProject, Bidproject, Account,Hirer_bid_select,KycInfo,Userprofile,country
from account.api.serializers import BidProjectSerializer,HirerSelectBidSerializer
from django.db.models import Avg
import json

from django.http import HttpResponse, JsonResponse, Http404



class BidRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            id = user.id

            email = user.email
            # print(email)
            data = {}
            project_code = request.data['project_code']
            project_bid = PostProject.objects.filter(project_code=project_code).values('id', 'project_title', 'description', 'min', 'max',
                                              'username', 'created_at','route','userid')

            for i in project_bid:

                if id == i['userid']:
                    data['message']="cant bid"
                    data['status']=102
                    return Response(data)
                else:
                    bid=Bidproject.objects.all()
                    no_of_bid = Bidproject.objects.filter(project_code=project_code).count()
                    user_kyc = KycInfo.objects.filter(userid=user.id)
                    if user_kyc.exists():
                        for kyc in user_kyc:
                            if kyc.kycstatus == 1:
                                data['message']="You have uploaded kyc details wait for approve"
                                data['status'] = 101
                                return Response(data)
                            elif kyc.kycstatus == 2:
                                data['message']="Your kyc is pending"
                                data['status'] = 101
                                return Response(data)
                            elif kyc.kycstatus == 3:
                                if bid.exists():
                                    mylist = []
                                    bid1 = Bidproject.objects.filter(project_code=project_code)
                                    for var in bid1:
                                        mylist.append(var.user_id)
                                        # print(var)

                                    if id in mylist:
                                        data['response'] = 'You have already bid for this project'
                                        data['status'] = 0
                                        return Response(data)

                                    else:
                                        serializer = BidProjectSerializer(data=request.data)
                                        data = {}
                                        if serializer.is_valid():
                                            bids = serializer.save()
                                            bids.project_name = i['route']
                                            bids.email = email
                                            bids.project_id = i['id']
                                            bids.user_id = id
                                            bids.no_of_bid = no_of_bid + 1
                                            user_bid = Account.objects.filter(id=id).values('bid')
                                            for e in user_bid:
                                                j = e['bid'] - 1
                                                user_bid.update(bid=j)
                                            bids.save()

                                            data['result'] = 'success'
                                            data['status'] = 101
                                        else:
                                            data = serializer.errors
                                            data['status'] = 0
                                        return Response(data)
                                else:
                                    serializer = BidProjectSerializer(data=request.data)
                                    data = {}
                                    if serializer.is_valid():
                                        bids = serializer.save()
                                        bids.project_name = i['route']
                                        bids.email = email
                                        bids.project_id = i['id']
                                        bids.user_id = id
                                        bids.no_of_bid = no_of_bid + 1
                                        user_bid = Account.objects.filter(id=id).values('bid')
                                        for e in user_bid:
                                            j = e['bid'] - 1
                                            user_bid.update(bid=j)
                                        bids.save()
                                        data['result'] = 'success'
                                        data['status'] = 101

                                    else:
                                        data = serializer.errors
                                        data['status'] = 0
                                    return Response(data)

                            else:
                                if kyc.kycstatus == 4:
                                    data['message']="Your kyc have been rejected"
                                    data['status'] = 0
                                    return Response(data)
                    else:
                        data['message']="kyc details not entered"
                        data['status']=0
                        return Response(data)

class HirerProjects(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user = request.user
        id = user.id
        mylist = []
        data1={}
        projects = PostProject.objects.filter(userid=id).values('id', 'project_title', 'description', 'min', 'max',
                                               'username','created_at','route','project_deadline','custom_budget').order_by('created_at').reverse()
        for i in projects:
            bidstatus = Bidproject.objects.filter(project_id=i['id']).filter(bid_status="Accepted").values( 'email', 'bid_amount', 'descreption')
            # bidselected = Hirer_bid_select.objects.filter(project_id=i['id']).values('freelancer_email_id')
            bid = Bidproject.objects.filter(project_id=i['id']).values('no_of_bid').count()

            averagebid = Bidproject.objects.filter(project_id=i['id']).values('bid_amount').aggregate(Avg('bid_amount'))

            if bidstatus.exists():
                data = {"projects": i,"freelancer_selected": bidstatus}
                mylist.append(data)
            else:
                data ={"projects": i, "bids": bid, "averagebid": averagebid}
                mylist.append(data)


        if projects.exists():
            data1['data'] = mylist
            data1['total'] = len(mylist)
            data1['message'] = 'success'
            data1['status'] = 100
            return Response(data1)
        else:
            data1['message'] = 'Not Found'
            data1['status'] = 102
            return Response(data1)

# class HirerProjects(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self,request):
#         user = request.user
#         id = user.id
#         mylist = []
#         data={}
#         data1={}
#         projects = PostProject.objects.filter(userid=id).values('id', 'project_title', 'description', 'min', 'max',
#                                                'username','created_at','route','project_deadline','custom_budget').order_by('created_at').reverse()
#         if projects.exists():
#
#             for i in projects:
#                 bidselected = Hirer_bid_select.objects.filter(project_id=i['id']).values('freelancer_email_id')
#
#                 bid = Bidproject.objects.filter(project_id=i['id']).values('no_of_bid').count()
#                 bidstatus = Bidproject.objects.filter(project_id=i['id']).values('bid_status')
#                 averagebid = Bidproject.objects.filter(project_id=i['id']).values('bid_amount').aggregate(Avg('bid_amount'))
#                 data = {"projects": i,   "bids": bid, "averagebid":averagebid,"freelancer selected":bidselected}
#                 mylist.append(data)
#                 data1['data'] = mylist
#                 data1['total'] = len(mylist)
#                 data1['message'] = 'success'
#                 data1['status'] = 100
#                 return Response(data1)
#         else:
#             data1['message'] = 'Not Found'
#             data1['status'] = 102
#             return Response(data1)



class Bid_Details_Project(APIView):
    permission_classes = (IsAuthenticated,)



    def get(self, request, projectroute):
        user=request.user
        id=user.id
        print(id)
        data = {}
        data1={}
        mylist=[]
        projects_posted = PostProject.objects.filter(route=projectroute).filter(userid=id).values('id', 'route', 'project_deadline','min', 'max')
        if projects_posted.exists():
            # print(projects_posted)
            # print("=============================")

            for i in projects_posted:
                norofbid = Bidproject.objects.filter(project_id=i['id']).count()
                biddeatils =Bidproject.objects.filter(project_id=i['id']).values('bid_amount','user_id','completion_time','email')
                # print(biddeatils)
                for j in biddeatils:
                    userdetails =  Userprofile.objects.filter(user_id=j['user_id']).values('user_name',  'profile',  'country_id','hourely_rate')
                    for k in userdetails:
                        data={ "username":k['user_name'],"profile":k['profile'],"location":country.objects.filter(id=k['country_id']).values('country_name'),
                               "email":j['email'],"bidamount":j['bid_amount'],"review":3,"hourely":k['hourely_rate'],"completiontime":j['completion_time'] ,"userid":j['user_id']}

                        mylist.append(data)

            data1['data']=mylist
            data1['total']=len(mylist)
            data1['message']="success"
            data1['status']=100
            return Response(data1)
        else:
            data1['message'] = "Not found"
            data1['status'] = 102
            return Response(data1)

class No_Of_Bid(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        id = user.id

        data1={}
        mylist = []
        biddetails = Bidproject.objects.filter(user_id=id).values('bid_amount', 'user_id', 'completion_time',
                                                                            'email', 'created_at','project_id')
        for var in biddetails:
            projectdetails = PostProject.objects.filter(id=var['project_id']).values('id', 'project_title', 'description', 'min', 'max',
                                               'username','created_at','route','project_deadline','custom_budget')
            for i in projectdetails:
                data={
                    "project":i ,
                      "bidamount": var['bid_amount'],"bidtime":var['created_at'],
                    "completiontime":var['completion_time']

                      }
                mylist.append(data)

        data1['data']=mylist
        data1['total']=len(mylist)
        return Response(data1)





class Select_Bid(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            employer = request.user
            employerid = employer.id
            projectroute = request.data['projectroute']
            freelancername = request.data['username']
            bidstatus = request.data['bidstatus']
            data = {}
            projectroute123 = PostProject.objects.filter(route=projectroute).filter(userid=employer.id).values()
            account = Account.objects.filter(username=freelancername).values()
            if projectroute123.exists():
                for j in projectroute123:
                    for i in account:
                        bid = Bidproject.objects.filter(project_id=j['id']).filter(user_id=i['id']).values()
                        if bid.exists():
                            biduser = Bidproject.objects.filter(project_id=j['id']).filter(bid_status="Accepted").values()
                            if biduser.exists():
                                data['message'] = 'Already freelancer selected'
                                data['status'] = 103
                                return Response(data)
                            else:

                                    bid.update(bid_status=bidstatus)
                                    projectroute345 = PostProject.objects.filter(route=projectroute).values()
                                    projectroute345.update(project_status=1)


                                    for i in account:
                                        freelancer_details = {
                                            "freelancer_id":i['id'],
                                            "freelancer_name":i['username'],
                                            "freelancer_email":i['email']
                                        }
                                        textdata=json.dumps(freelancer_details)

                                        print(textdata)
                                    filepath = '/root/Homestead/artomate/artomate/src/chatfile/Emp' + str(employerid) + '_TO_Fre' + str(i['id']) + '.json'
                                    with open(filepath, "w") as f:
                                        f.writelines(textdata)
                                    data['message'] = 'success'
                                    data['status'] = 100
                                    return Response(data)
                        else:
                            data['message'] = 'He has not bid for this project'
                            data['status'] = 103
                            return Response(data)
            else:
                data['message']='Cant select'
                data['status']=106
                return Response(data)


class ChatView(APIView):
    def get(self,request):
        # filepath=Emp2_TO_Fre4.json'
        with open('/root/Homestead/artomate/artomate/src/chatfile/Emp2_TO_Fre4.json', "r") as f:
            data=json.load(f)
            # print(data)

        return Response(data)


class ChatReply(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self,request):
        datatext =request.data




        with open('/root/Homestead/artomate/artomate/src/chatfile/Emp2_TO_Fre4.json', "a") as f:
            f.writelines(json.dumps(datatext))
        return Response("done")













