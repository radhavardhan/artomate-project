from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import TicketCat,RaiseTicket
from account.api.serializers import  RaiseTicketSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated



class TicketTypeView(APIView):
    def get(self, request):
        tickettype = TicketCat.objects.all().values('id','name')
        data={}
        data['ticketcategory'] = tickettype
        return Response(data)

class Raiseticket(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        id = user.id

        serializer = RaiseTicketSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            ticket = serializer.save()
            ticket.user_id = id
            ticket.save()
            data['message'] = "Success"
            data['status'] = 100
        else:
            data['error'] = serializer.errors()
            data['status'] = 102
        return Response(data)

class TicketView(APIView):
    def get(self, request):
        ticket = RaiseTicket.objects.filter(user_id=1).values('id','tickettype', 'user_id', 'description')
        data={}
        data['ticketlist'] = ticket
        data['status'] = 100
        return Response(data)
