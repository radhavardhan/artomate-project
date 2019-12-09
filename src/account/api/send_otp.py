import os,random
from twilio.rest import Client
from rest_framework.views import APIView
from rest_framework.response import Response


class TWILIOSendOTP(APIView):

    def post(self,request,*args,**kwargs):
        phone_number = request.data['phone']
        print(phone_number)
        account_sid = "AC9f09b80ceb33e54517ed9ed3a9cb5b7c"
        auth_token = "a68e1fc3be2a8e361e32ab8f28be2f05"

        client = Client(account_sid,auth_token)
        key = random.randint(999, 9999)
        OTP = 'your Otp is  '+ str(key)
        print(OTP)
        client.messages.create(
            to = phone_number,
            from_ = "+12533368296",
            body =OTP,
        )
        return Response('done')


