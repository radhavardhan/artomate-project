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


class KycView(APIView):
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        if request.method == 'POST':
            user = request.user
            if not user:
                return Response({'error': 'Invalid Credentials'}, status=HTTP_200_OK)

            else:

                id = user.id
                postpro = KycInfo.objects.filter(userid=id)

                if postpro.exists():
                    for kycstat in postpro:
                        serializer = KYCInfoSerializer(data=request.data)
                        data = {}
                        if kycstat.kycstatus == 1:
                            data['result'] = 'allready entered kyc details'
                            data['status'] = 0
                else:
                    serializer = KYCInfoSerializer(data=request.data)
                    data = {}
                    if serializer.is_valid():
                        kyc = serializer.save()
                        kyc.username = user.username
                        kyc.userid = user.id
                        kyc.kycstatus = 1
                        kyc.save()
                        data['result'] = 'success'
                        data['status'] = 1
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
