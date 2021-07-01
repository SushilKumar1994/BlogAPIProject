from django.shortcuts import render

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny


from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import *

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import generics

from rest_framework.decorators import permission_classes,api_view

from django.http import Http404

from rest_framework import status

import json


# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),                 #to solve decode error-->pip install PyJWT==1.7.1
        'access': str(refresh.access_token),
    }


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreate(APIView):
    permission_classes = [AllowAny,]

    @csrf_exempt
    def post(self, request, format='json'):
        user=None
        data = request.data
        serializer = UserSerializer(data={'email':data['email'],'password':data['password']})
        
        if serializer.is_valid():
            user = serializer.save()
            if user:
                user.save()

                try:
                    UserProfile.objects.create(user=user,first_name=data['first_name'],last_name=data['last_name'],username=data['username'])

                    return Response({"msg":"User profile has been created Successfully"},status=200)

                except Exception as e: 
                    if user !=None:
                        '''if there is any error while creating user profile,delete the created user too'''
                        user.delete()
                    if 'unique constraint' in str(e) or 'UNIQUE constraint' in str(e) :
                        return Response({"msg":"That username is taken.Try another"},status=400)

                    else:
                        return Response({"msg":str(e)},status=400)
                    
        return Response(serializer.errors, status=500)

class LoginView(APIView):
    permission_classes = [AllowAny,]
    def post(self,request,format="json"):
        data = request.data
        print(data)
        try:
            user = User.objects.get(email=data['email'])

            if user.check_password(data['password']):
                print("correct password")
                                
                token = get_tokens_for_user(user=user)
                
                print("token=",token)

                return Response(token,status=200)

            else:
                print("invalid password")
                return Response({"detail":"Wrong password."},status=400)

        except User.DoesNotExist:
            print("not present")
            return Response({"detail":"Please Register to continue"},status=400)

        
class GetUserProfileData(generics.ListAPIView):
    serializer_class=UserProfileSerializer
    permission_classes=[IsAuthenticated,]

    def get_queryset(self):
        queryset=UserProfile.objects.filter(user=self.request.user)
        return queryset

class UpdateUserAPIView(generics.UpdateAPIView):   #patchapi
    queryset=UserProfile.objects.all()
    serializer_class=UpdateUserProfileSerializer
    lookup_field="id"
    permission_classes=[IsAuthenticated,] 

    def perform_update(self,serializer):
        serializer.save(user=self.request.user)

class PostCreateAPIView(generics.CreateAPIView):
    queryset=Post.published.all()
    serializer_class=PostCreateUpdateSerializer
    permission_classes=[IsAuthenticated,]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class PostListAPIView(generics.ListAPIView):    
    queryset=Post.published.all()
    serializer_class=PostListSerializer
    permission_classes=[AllowAny,]
    search_fields=['title']
    # ordering_fields=['id']

#
    
class PostDetailAPIView(generics.RetrieveAPIView):
    queryset=Post.published.all()
    serializer_class=PostDetailSerializer
    lookup_field="id"
    permission_classes=[IsAuthenticated,]


class PostUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset=Post.published.all()
    serializer_class=PostCreateUpdateSerializer
    lookup_field="id"
    permission_classes=[IsAuthenticated,]

    def perform_update(self,serializer):
        serializer.save(user=self.request.user)

class PostDeleteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get_object(self, id):
        try:
            return Post.published.get(id=id)
        except Post.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        obj = self.get_object(id)

        obj.delete()
        return Response({"msg":"Post has been deleted successfully"},status=status.HTTP_204_NO_CONTENT)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentCreateSerializer
    permission_classes=[IsAuthenticated,]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class CommentListAPIView(generics.ListAPIView):
    queryset=Comment.objects.filter(id__gte=0)
    serializer_class=CommentListSerializer
    permission_classes=[AllowAny]
    search_fields=['title']

class CommentUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentUpdateSerializer
    permission_classes=[IsAuthenticated]
    lookup_field="id"

    def perform_update(self,serializer):
        serializer.save(user=self.request.user)


class CommentDeleteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get_object(self, id):
        try:
            return Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        obj = self.get_object(id)

        obj.delete()
        return Response({"msg":"Comment has been deleted successfully"},status=status.HTTP_204_NO_CONTENT)

