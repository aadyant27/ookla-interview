import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, EmailSerializer
from .models import User

# SWAGGER
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import jwt
from dotenv import load_dotenv
load_dotenv()


@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all users.",
    responses={200: UserSerializer(many=True)}
)
@api_view(['GET'])
def get_users(request):
    try:
        if request.method == 'GET':
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)

            return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='post',
    operation_description="Create a new user.",
    request_body=UserSerializer,
    responses={
        201: openapi.Response(description="User successfully created"),
        400: openapi.Response(description="Bad request")
    }
)
@api_view(['POST'])
def create_user(request):
    try:
        if request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['email'] = serializer.validated_data['email'].lower(
                )
                serializer.save()
                return Response({'message': 'User successfully created'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='post', request_body=EmailSerializer, responses={200: openapi.Response('JWT token', schema=openapi.Schema(type='object', properties={'JWT token': openapi.Schema(type='string')}))})
@api_view(['POST'])
def create_token(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        # Extract email from body
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            payload = {
                'email': email,
                'phone': user.phone,
                'is_admin': user.is_admin
            }
            token = jwt.encode(payload, os.environ.get(
                'JWT_SECRET_KEY'), algorithm='HS256')

            return Response({"JWT token": token}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
