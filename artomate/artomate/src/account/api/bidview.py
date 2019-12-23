from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import PostProject, Bidproject, Account,Hirer_bid_select
from account.api.serializers import BidProjectSerializer,HirerSelectBidSerializer
import json


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
            # print(no_of_bid)
            if bid.exists():
                mylist = []
                bid1 = Bidproject.objects.filter(project_code=project_code)
                for var in bid1:
                    mylist.append(var.user_id)
                    # print(var)

                if id in mylist:
                    data['response'] = 'You have already bid for this project'
                    return Response(data)

                else:
                    serializer = BidProjectSerializer(data=request.data)
                    data = {}
                    if serializer.is_valid():
                        bids = serializer.save()
                        bids.project_name = project_bid.project_title
                        bids.email=email
                        bids.project_id = project_bid.id
                        bids.user_id = id
                        bids.no_of_bid = no_of_bid + 1
                        bids.save()
                        data['result'] = 'success'
                        data['status'] = 1
                    else:
                        data = serializer.errors
                        data['status'] = 0
                    return Response(data)
            else:
                serializer = BidProjectSerializer(data=request.data)
                data = {}
                if serializer.is_valid():
                    bids = serializer.save()
                    bids.project_name = project_bid.project_title
                    bids.email = email
                    bids.project_id = project_bid.id
                    bids.user_id = id
                    bids.no_of_bid = no_of_bid + 1
                    bids.save()
                    data['result'] = 'success'
                    data['status'] = 1
                else:
                    data = serializer.errors
                    data['status'] = 0
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



    def get(self, request, projectcode):

        print(projectcode)
        if not permission_classes:
            return Response({'error': 'Invalid Credentials'}, status=HTTP_200_OK)
        else:

            projects_posted = PostProject.objects.filter(project_code=projectcode).values('id', 'route', 'project_deadline','min','max')
            biddeatils =Bidproject.objects.filter(project_code=projectcode).values('bid_amount','user_id','completion_time','email')
            norofbid=Bidproject.objects.filter(project_code=projectcode).count()
            for var in biddeatils:

                data={}
                data['project']=projects_posted
                data['no_of_bid']=norofbid
                data['bid details']=biddeatils
                # data['user details']=Account.objects.filter(id=var['user_id']).values('username')
            return Response(data)



class Select_Bid(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if request.method=='POST':
            projectid=request.data['project_id']
            projectcheck = Hirer_bid_select.objects.filter(project_id=projectid)
            data={}
            if projectcheck.exists():
                data['result'] = 'Allready freelancer selected for project'
                data['status'] = 0
            else:
                projectroute = PostProject.objects.get(id=projectid)
                print(projectroute)
                serializer=HirerSelectBidSerializer(data=request.data)
                if serializer.is_valid():
                    print(123)
                    selectedbid=serializer.save()
                    selectedbid.project_route = projectroute.route
                    selectedbid.hirer_email_id = request.user.email
                    selectedbid.save()
                    data['result'] = "success"
                    data['status'] = 1
                else:
                    data['error'] = serializer.errors
                    data['status'] = 0

            return Response(data)

