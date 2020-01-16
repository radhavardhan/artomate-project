from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import PostProject, Bidproject, Account,Hirer_bid_select,KycInfo,Userprofile
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
            project_bid = PostProject.objects.get(project_code=project_code)
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
                                    bids.project_name = project_bid.route
                                    bids.email = email
                                    bids.project_id = project_bid.id
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
                                bids.project_name = project_bid.route
                                bids.email = email
                                bids.project_id = project_bid.id
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




class No_Of_Bid(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        id = user.id

        mylist = []
        projects_posted = PostProject.objects.filter(userid=id).values('project_title', 'route', 'id')
        # print(projects_posted)
        for var in projects_posted:

            data={"project":var['route'],"no_of_bid":Bidproject.objects.filter(project_id=var['id']).count()}
            mylist.append(data)



        return Response(mylist)


class Bid_Details_Project(APIView):
    permission_classes = (IsAuthenticated,)



    def get(self, request, projectroute):
        print(projectroute)
        projects_posted = PostProject.objects.filter(route=projectroute).values('id', 'route', 'project_deadline','min','max')

        for i in projects_posted:
            biddeatils =Bidproject.objects.filter(project_id=i['id']).values('bid_amount','user_id','completion_time','email')
            norofbid=Bidproject.objects.filter(project_id=i['id']).count()
            data={}
            data['project']=projects_posted
            data['no_of_bid']=norofbid
            data['bid details']=biddeatils
            return Response(data)



class Select_Bid(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if request.method=='POST':
            data = {}
            if 'project_id' in request.data:
                projectid=request.data['project_id']
                if not projectid:
                    data['message'] = "enter an project_id"
                    data['status'] = 102
                    return Response(data)
                else:
                    projectcheck = Hirer_bid_select.objects.filter(project_id=projectid)
                    if projectcheck.exists():
                        data['message'] = 'Allready freelancer selected for project'
                        data['status'] = 102
                    else:
                        # freelancer_email = request.data['freelancer_email_id']
                        # biddetails=Bidproject.objects.filter(email=freelancer_email)
                        # if biddetails.exists():
                        projectroute = PostProject.objects.get(id=projectid)
                        print(projectroute)
                        serializer=HirerSelectBidSerializer(data=request.data)
                        if serializer.is_valid():
                            print(123)
                            selectedbid=serializer.save()
                            selectedbid.project_route = projectroute.route
                            selectedbid.hirer_email_id = request.user.email
                            selectedbid.save()
                            data['message'] = "success"
                            data['status'] = 100
                        else:
                            data['error'] = serializer.errors
                            data['status'] = 0
                    return Response(data)
            else:
                data['message'] = "project_id required"
                data['status'] = 102
                return Response(data)


