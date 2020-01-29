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
        user=request.user
        id=user.id
        projects =PostProject.objects.filter(userid=id).values('id', 'project_title', 'description', 'min', 'max',
                                               'username','created_at','route','project_deadline','custom_budget').order_by('created_at').reverse()
        data={}
        data['projects']=projects
        data['total']=len(projects)
        data['message']='success'

        data['status']=100
        return Response(data)



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
            print(projects_posted)
            print("=============================")

            for i in projects_posted:
                norofbid = Bidproject.objects.filter(project_id=i['id']).count()
                biddeatils =Bidproject.objects.filter(project_id=i['id']).values('bid_amount','user_id','completion_time','email')
                print(biddeatils)
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

    def get(self,request,projectid,userid):
        if request.method=='GET':
            user =request.user
            useremail=user.email

            data = {}
            projectroute = PostProject.objects.filter(id=projectid).values()

            userdetails = Userprofile.objects.filter(id=userid).values('user_name', 'designation', 'hourely_rate',
                                                    'profile', 'user_id', 'country_id')
            account = Account.objects.filter(id=userid).values()
            print(projectroute)
            for i in projectroute:
                for j in account:
                    details = Hirer_bid_select.objects.create( hirer_email_id=useremail,project_id=i['id'],project_route=i['route'],freelancer_email_id=j['email'])
                    details.save()

            projectroute = PostProject.objects.get(id=projectid)
            projectroute.project_status = 1
            projectroute.save()
            data['message'] = "success"
            data['status'] = 100
            return Response(data)



