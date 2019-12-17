from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import PostProject, Bidproject, Account
from account.api.serializers import BidProjectSerializer
import json


class BidRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            id = user.id
            data = {}
            project_code = request.data['project_code']
            project_bid = PostProject.objects.get(project_code=project_code)

            # print(project_bid.id)
            bid = Bidproject.objects.filter(project_code=project_code)
            no_of_bid = Bidproject.objects.filter(project_code=project_code).count()
            # print(no_of_bid)
            mylist = []
            for var in bid:
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
                    # print('done')
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
        data = {}
        mylist = []
        projects_posted = PostProject.objects.filter(userid=id).values('project_title', 'route', 'id')
        # print(projects_posted)
        for var in projects_posted:
            numberofbids = Bidproject.objects.filter(project_id=var['id']).count()
            bidu_ser_id = Bidproject.objects.filter(project_id=var['id']).values('id', 'user_id')
            mylist.append(var['route'])
            mylist.append(numberofbids)

            # for var2 in bidu_ser_id:
            #     biduserid=var2['user_id']
            #     # print(biduserid)

        return Response(mylist)


class Bid_Details_Project(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, projectcode):
        print(projectcode)

        projects_posted = PostProject.objects.filter(project_code=projectcode).values( 'route', 'project_deadline','min','max')
        biddeatils =Bidproject.objects.filter(project_code=projectcode).values('bid_amount','user_id','completion_time','email')
        norofbid=Bidproject.objects.filter(project_code=projectcode).count()
        for var in biddeatils:

            data={}
            data['project']=projects_posted
            data['no_of_bid']=norofbid
            data['bid details']=biddeatils
            data['user details']=Account.objects.filter(id=var['user_id']).values('username')
        return Response(data)
