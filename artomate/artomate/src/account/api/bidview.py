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
            bid = Bidproject.objects.filter(project_id=i['id']).values('no_of_bid').count()
            averagebid = Bidproject.objects.filter(project_id=i['id']).values('bid_amount').aggregate(Avg('bid_amount'))

            data = {"projects": i,   "bids": bid, "averagebid":averagebid}
            mylist.append(data)
        print(mylist)

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
#                 bidselected = Hirer_bid_select.objects.filter(project_id=i['id']).values()
#                 if bidselected.exists():
#                     for k in bidselected:
#                         data['message']="freelancer selected"
#                         data['details'] = k['freelancer_email_id']
#                         data['status'] = 104
#                         return Response(data)
#                 else:
#                     bid = Bidproject.objects.filter(project_id=i['id']).values('no_of_bid').count()
#                     bidstatus = Bidproject.objects.filter(project_id=i['id']).values('bid_status')
#                     averagebid = Bidproject.objects.filter(project_id=i['id']).values('bid_amount').aggregate(Avg('bid_amount'))
#                     data = {"projects": i,   "bids": bid, "averagebid":averagebid}
#                     mylist.append(data)
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

    def post(self,request):
        if request.method=='POST':
            user =request.user
            useremail=user.email
            projectroute =request.data['projectroute']
            username = request.data['username']
            bidstatus = request.data['bidstatus']
            data = {}
            projectroute123 = PostProject.objects.filter(route=projectroute).values()

            account = Account.objects.filter(username=username).values()
            if projectroute123.exists():
                print(1)
                for j in projectroute123:
                    print(2)
                    bid = Bidproject.objects.filter(project_id=j['id']).values()
                    print(bid)
                    for k in bid:
                        print(k)
                        if k['bid_status'] == "Accepted":
                            print(4)
                            data['message'] = "already selected freelancer for this project"
                            data['status'] = 102
                            return Response(data)
                        else:
                            print(5)
                            for i in account:
                                print(6)
                                if bidstatus=='Accepted':
                                        print(7)

                                        details = Hirer_bid_select.objects.create(hirer_email_id=useremail, project_id=j['id'],
                                                                                  project_route=j['route'],
                                                                                  freelancer_email_id=i['email'])
                                        details.save()


                                        bid = Bidproject.objects.filter(project_id=j['id']).filter(user_id=i['id']).values()
                                        if bid.exists():
                                            print(8)
                                            bid.update(bid_status=bidstatus)
                                            projectroute345 = PostProject.objects.filter(route=projectroute).values()

                                            projectroute345.update(project_status=1)
                                        else:
                                            print(10)
                                            data['message']="He has not bid for this project"
                                            data['status']=102
                                            return Response(data)
                                else:
                                    print(11)
                                    bid = Bidproject.objects.filter(project_id=j['id']).filter(user_id=i['id']).values()
                                    bid.update(bid_status=bidstatus)
                                    projectroute345 = PostProject.objects.filter(route=projectroute).values()

                                    projectroute345.update(project_status=0)

                    data['message'] = "success"
                    data['status'] = 100
                    return Response(data)
            else:
                print(12)
                data['message']="Not Found"
                data['status']=102
                return Response(data)



