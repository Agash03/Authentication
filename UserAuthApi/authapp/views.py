from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authapp.serilalizers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
                                   
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request, Format= None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token  = get_tokens_for_user(user)
            return Response({'token':token,'msg':'User Registered Successfully'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, QUESTstatus=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self, request, Format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        email=serializer.data.get('email')
        password=serializer.data.get('password')
        user = authenticate(email = email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'User Login Successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
class UserProfileView(APIView):
    permission_classes= [IsAuthenticated] 
    def get(self, request, Format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangepassword(APIView):
    permission_classes= [IsAuthenticated]
    def post(self, request, Format=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user': request.user})
        #serializer = UserChangePasswordSerializer(data=request.data, context={'request':request})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, QUESTstatus=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    def post(self, request, Format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Reset password link send to your email'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    def post(self, request, uid, token,Format=None):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid': uid , 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)