from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import PostProject,Bidproject,Account
from account.api.serializers import  BidProjectSerializer

class BidRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            id = user.id
            data = {}
            project_code = request.data['project_code']
            project_bid = PostProject.objects.get(project_code=project_code)

            print(project_bid.id)
            bid = Bidproject.objects.filter(project_code=project_code)
            no_of_bid = Bidproject.objects.filter(project_code=project_code).count()
            print(no_of_bid)
            mylist = []
            for var in bid:
                mylist.append(var.user_id)
                print(var)

            if id in mylist:
                data['response'] = 'You have already bid for this project'
                return Response(data)

            else:
                serializer = BidProjectSerializer(data=request.data)
                data = {}
                if serializer.is_valid():
                    bids = serializer.save()
                    bids.project_name = project_bid.project_title
                    print('done')
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
    def get(self, request,project_code):

        data = {}
        data['Total number of bids on project'] = Bidproject.objects.filter(project_code=project_code).count()
        Project_Details = Bidproject.objects.filter(project_code=project_code).values('project_name','bid_amount','email','user_id')
        mylist = list(Project_Details)
        Bid_project_details=[]
        for i in mylist:
            user_id=i['user_id']
            bid_username = Account.objects.filter(id=user_id).values('username')
            # print(user_id)
            Bid_project_details.append(i)
            Bid_project_details.append(bid_username)


        data['project'] = list(Bid_project_details)

        return Response(data)
