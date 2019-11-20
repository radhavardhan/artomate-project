# class KycView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         if request.method == 'POST':
#             user = request.user
#             id = user.id
#             postpro = KycInfo.objects.filter(userid=id)
#             print(id)
#             if postpro.exists():
#                 for kycstat in postpro:
#                     serializer = KYCInfoSerializer(data=request.data)
#                     data = {}
#                     if kycstat.kycstatus == 1:
#                         data['result'] = 'allready entered kyc details'
#                         data['status'] = 0
#             else:
#                 serializer = KYCInfoSerializer(data=request.data)
#                 data = {}
#                 if serializer.is_valid():
#                     kyc = serializer.save()
#                     kyc.username = user.username
#                     kyc.userid = user.id
#                     kyc.kycstatus = 1
#                     kyc.save()
#                     data['result'] = 'success'
#                     data['status'] = 1
#                 else:
#                     data['status'] = 0
#                     data = serializer.errors
#         return Response(data)
