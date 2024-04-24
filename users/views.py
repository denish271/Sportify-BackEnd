# from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User,Product,Cart,Address,Payment,Order,Review
from .serializers import Userserializer,ProductSerializer,CartSerializer,AdressSerializer,PaymentSerializer,OrderSerializer,UserForgetSerializer,ReviewSerializer
import jwt, datetime
# import razorpay
from django.conf import settings
from .constants import PaymentStatus


# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer = Userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User Not Found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        name = user.name
        id=user.id
        
        # payload ={
        #     "id" : user.id,
        #     'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        #     "iat" : datetime.datetime.utcnow()
        # }

        # token = jwt.encode(payload,'secret',algorithm='HS256')
        
        response = Response()

        # response.set_cookie(key='jwt',value=token,httponly=True)

        response.data = {
            # 'jwt' : token
            'msg' : 'success',
            'id' : id,
            'name' : name,
            'email' : email
        }

        return response
    
class ForgetPassView(APIView):
    def post(self,request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User Not Found")
        id=user.id
        return Response({
            'msg' : 'success',
            "id" : id
        })
    
class RazorpayView(APIView):
    def post(self,request):
        # if request.method == "POST":
        name = request.data["name"]
        amount = request.data["amount"]
        print(name,amount)
            # client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            # razorpay_order = client.order.create(
            #     {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
            # )
            # print(razorpay_order)
            # # order = Order.objects.create(
            # #     name=name, amount=amount, provider_order_id=payment_order["id"]
            # # )
            # # order.save()
        return Response({
        'msg' : 'success',
        "data": {
            name, amount, 
        }
        })
        # return Response({
        #     'msg' : 'fail',
        # })


# @csrf_exempt
# def callback(request):
#     def verify_signature(response_data):
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         return client.utility.verify_payment_signature(response_data)

#     if "razorpay_signature" in request.POST:
#         payment_id = request.POST.get("razorpay_payment_id", "")
#         provider_order_id = request.POST.get("razorpay_order_id", "")
#         signature_id = request.POST.get("razorpay_signature", "")
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.signature_id = signature_id
#         order.save()
#         if not verify_signature(request.POST):
#             order.status = PaymentStatus.SUCCESS
#             order.save()
#             return Response({
#             'msg' : 'success',
#             "context" : order.status
#             })
        
#         else:
#             order.status = PaymentStatus.FAILURE
#             order.save()
#             return Response({
#             'msg' : 'fail',
#             "context" : order.status
#             })
#     else:
#         payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#         provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
#             "order_id"
#         )
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.status = PaymentStatus.FAILURE
#         order.save()
#         return Response({
#             'msg' : 'fail',
#             "context" : order.status
#             })

class ForgetChangePassView(APIView):
    def patch(self,request,pk):
        try:
            user_id = User.objects.get(pk=pk)
        except :
            return Response({'msg' : "user Not Found"})
        p = make_password(request.data['password'])
        request.data['password'] = p
        serializer = UserForgetSerializer(user_id,data = request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ChangePassword(APIView):
    def patch(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except :
            raise {'msg' : "user Not Found"}
        
        old_pass = request.data['old_pass']

        if not user.check_password(old_pass):
            raise AuthenticationFailed("Incorrect Old Password")

        p = make_password(request.data['password'])
        request.data['password'] = p
        serializer = UserForgetSerializer(user,data = request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# class UserView(APIView):
#     def get(self,request):
#         token = request.COOKIES.get('jwt')

#         if not token:
#             raise AuthenticationFailed("Unauthenticated")

#         try:
#             payload= jwt.decode(token,'secret',algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Unauthenticated")

#         user = User.objects.filter(id = payload['id']).first()
#         serializer = Userserializer(user)

#         return Response(serializer.data)
    
# class LogoutView(APIView):
#     def post(self,request):
#         responce = Response()
#         responce.delete_cookie('jwt')
#         responce.data = {
#             "msg" : "success"
#         }
#         return responce
    
class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class AddressView(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AdressSerializer
# class CartCreateView(APIView):
#     def get(self, request, format=None):
#         cart_items = Cart.objects.all()
#         serializer = CartSerializer(cart_items, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

# class CartView(APIView):
#     def get_object(self, pk):
#         try:
#             return Cart.objects.get(pk=pk)
#         except Cart.DoesNotExist:
#             raise {'msg' : 'Id is Not Found'}

#     def get(self, request, pk, format=None):
#         cart_item = self.get_object(pk)
#         serializer = CartSerializer(cart_item)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         cart_item = self.get_object(pk)
#         serializer = CartSerializer(cart_item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

#     def delete(self, request, pk, format=None):
#         cart_item = self.get_object(pk)
#         cart_item.delete()
#         return Response()