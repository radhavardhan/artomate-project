from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import KycInfo,country,Experiance
from account.api.serializers import  KYCInfoSerializer
from mysite import settings


class KycView(APIView):
    permission_classes = (IsAuthenticated,)



    def post(self, request):
        data = {}
        if request.method == 'POST':
            user = request.user

            id = user.id
            postpro = KycInfo.objects.filter(userid=id)

            if postpro.exists():
                for kycstat in postpro:

                    data = {}
                    if kycstat.kycstatus == 1:
                        data['result'] = 'allready entered kyc details'
                        data['status'] = 0
            else:
                serializer = KYCInfoSerializer(data=request.data)

                if serializer.is_valid():
                    kyc = serializer.save()
                    kyc.username = user.username
                    kyc.userid = user.id
                    kyc.kycstatus = 1
                    kyc.save()
                    data['result'] = 'success'
                    data['status'] = 1
                    return Response(data)
                else:
                    data['status'] = 0
                    data = serializer.errors
            return Response(data)



class CountryView(APIView):
    def get(self, request):
        country1 = country.objects.all().values('id', 'country_name')
        data = {}
        data['countries'] = country1
        return Response(data)

class ExperianceView(APIView):
    def get(self, request):
        exp = Experiance.objects.all().values('id', 'Exp_name')
        data = {}
        data['experiance'] = exp
        return Response(data)

class KycStatusView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user=request.user
        kycstatus = KycInfo.objects.filter(userid=user.id)

        if kycstatus.exists():
            for var in kycstatus:
                if  var.kycstatus == 1:
                    return Response({ 'kyc_message': 'kyc details uploaded', 'kyc_status': 1},
                                    status=HTTP_200_OK)
                else:
                    if  var.kycstatus  == 2:
                        return Response({'kyc_message': 'kyc details pending', 'kyc_status': 2},
                                    status=HTTP_200_OK)
                    else:
                        if  var.kycstatus  == 3:
                            return Response({ 'kyc_message': 'kyc details approved', 'kyc_status': 3},
                                        status=HTTP_200_OK)
                        else:
                            if  var.kycstatus  == 4:
                                return Response({ 'kyc_message': 'kyc details rejected', 'kyc_status': 4},
                                                status=HTTP_200_OK)
        return Response({ 'kyc_message': 'kyc details not entered', 'kyc_status': 0},
                        status=HTTP_200_OK)
