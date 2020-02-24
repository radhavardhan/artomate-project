from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from mysite.settings import BASE_DIR
import json
from account.models import PostProject, Bidproject,Account
from account.api.serializers import BidProjectSerializer, HirerSelectBidSerializer

class TestJson(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        employer = request.user
        employerid = employer.id

        data={}
        freelancerid = 12
        pickup_records = []
        textdata=request.data['record']
        filepresent = BASE_DIR + '/Emp' + str(employerid) + '_TO_Fre' + str(
            freelancerid) + '.json'


        filepath = BASE_DIR + '/Emp' + str(employerid) + '_TO_Fre' + str(
        freelancerid) + '.json'


        pickup_records.append(textdata)
        pickup_records = json.dumps(pickup_records, indent=4)
        with open(filepath, "a") as f:
            f.write(json.dumps(textdata))
        pickup_response = json.loads(pickup_records)
        return Response(pickup_response)



class ChatView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        data={}
        mylist=[]
        data1={}
        currentuser = request.user
        # id=currentuser.id
        id = 2
        employerid = 2
        freelancerid = 3
        Employer = PostProject.objects.filter(userid=id).values()
        freelancer =Bidproject.objects.filter(user_id=id).values()
        filepath = '/root/Homestead/artomate/artomate/src/chat_folder' + '/Emp' + str(employerid) + '_TO_Fre' + str(
            freelancerid) + '.json'
        filepath2 = '/root/Homestead/artomate/artomate/src/chat_folder/Emp2_TO_Fre4.json'
        if Employer.exists():
            empid='Emp'+ str(id)
            if empid  in filepath:
                newlist = []
                for line in open(filepath, 'r'):
                    newlist.append(json.loads(line))
                for line in open(filepath2,'r'):
                    newlist.append(json.loads(line))
                for i in newlist:
                    data={"projectroute":i['projectroute'],"freelancer":i['freelancer_id'],"freelancer_message":i['freelancer_message'],"employer_message":i['hierer_message']}
                    mylist.append(data)
                data1['employer_chat']=mylist
                return Response(data1)
            else:
                return Response("no file")
        else:
            freid = 'Fre' + str(id)
            if freid in filepath:
                newlist = []
                for line in open(filepath, 'r'):
                    newlist.append(json.loads(line))
                for i in newlist:
                    data = {"projectroute": i['projectroute'], "employerid": i['hierer_id'],"hierer_message":i['hierer_message'],"freelancer_message":i['freelancer_message'],}
                    mylist.append(data)
                data1['freelancer_chat'] = mylist
                return Response(data1)
            else:
                return Response("no file")


class ChatReply(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request,projectroute):
        data = {}
        mylist = []
        data1 = {}
        currentuser = request.user
        currentuser = request.user
        # id=currentuser.id
        id = 4
        datatext = request.data
        account = Account.objects.filter(id=id).values()
        Employer = PostProject.objects.filter(userid=id).filter(route=projectroute).values()
        # print(Employer)
        freelancer = Bidproject.objects.filter(user_id=id).values()


        bidprojectdetail= Bidproject.objects.filter(user_id=id).filter(project_name=projectroute).values()
        # print(bidprojectdetail)

        employerid = 2
        freelancerid = 4

        filepath = '/root/Homestead/artomate/artomate/src/chat_folder' + '/Emp' + str(employerid) + '_TO_Fre' + str(
            freelancerid) + '.json'
        filepath2 = '/root/Homestead/artomate/artomate/src/chat_folder/Emp2_TO_Fre4.json'

        if Employer.exists():
            print("if")
            empid = 'Emp' + str(id)
            if empid in filepath:
                print(1)
                newlist = []
                projectroute123 = PostProject.objects.filter(route=projectroute).values()
                for j in projectroute123:
                    for i in account:
                        bida_ccept_details = {
                            "freelancer_id": freelancerid,
                            "hierer_id": i['id'],
                            "freelancer_message": "",
                            "hierer_message": datatext['employer_message'],
                            "isWho": 1,
                            "projectroute": j['route'],
                            "project_id": j['id'],

                        }
                    print(bida_ccept_details)
                with open(filepath, "a") as f:
                    f.write(json.dumps(bida_ccept_details))

                return Response("done")
            else:
                return Response("no file")
        else:
            print(2)
            freid = 'Fre' + str(id)
            if freid in filepath:
                projectroute123 = PostProject.objects.filter(route=projectroute).values()
                for j in projectroute123:
                    for i in account:
                        bida_ccept_details = {
                            "freelancer_id": freelancerid,
                            "hierer_id": i['id'],
                            "freelancer_message": datatext['freelancer_message'],
                            "hierer_message": "",
                            "isWho": 0,
                            "projectroute": j['route'],
                            "project_id": j['id'],

                        }
                    print(bida_ccept_details)

                with open(filepath, "a") as f:
                    f.write(json.dumps(bida_ccept_details))
                return Response("done")
            else:
                return Response("nofile freelancer")


