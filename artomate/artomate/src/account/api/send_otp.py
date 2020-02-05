import os,random
from twilio.rest import Client
from rest_framework.views import APIView
from rest_framework.response import Response
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings

# import zerosms


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


# class SendOtp(APIView):
#     def post(self,request):
#         phone_number = request.data['phone']
#         key = random.randint(999, 9999)
#         OTP = 'your Otp is  ' + str(key)
#
#         zerosms.sms(message='your Otp is  ' + str(key), receivernum=phone_number)
#         return Response('done')
#




#this is your "password/ENCRYPT_KEY". keep it in settings.py file
#key = Fernet.generate_key()
class Encrypt(APIView):

    def post(self,request):
        try:
            # convert integer etc to string first
            text = request.data['password']
            txt = str(text)
            print(txt)
            # get the key from settings
            cipher_suite = Fernet(settings.ENCRYPT_KEY)
            print(cipher_suite)# key should be byte
            # #input should be byte, so convert the text to byte
            encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
            print(encrypted_text)
            # encode to urlsafe base64 format
            encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
            print(encrypted_text)
            return Response(encrypted_text)
        except Exception as e:
            # log the error if any
            logging.getLogger("error_logger").error(traceback.format_exc())
            return Response("error")

class Decreypt(APIView):

    def get(self,request,txt):
        try:
            # base64 decode
            txt = base64.urlsafe_b64decode(txt)
            print(txt)
            cipher_suite = Fernet(settings.ENCRYPT_KEY)
            print(cipher_suite)
            decoded_text = cipher_suite.decrypt(txt).decode("ascii")
            print(decoded_text)
            return Response(decoded_text)
        except Exception as e:
            # log the error
            logging.getLogger("error_logger").error(traceback.format_exc())
            return Response("erorr")



