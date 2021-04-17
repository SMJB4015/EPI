from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from store.models import *
from django.http import JsonResponse
from store.serializers import ClientSerializer, ProduitSerializer,  CategorieSerializer, UserSerializer,UserSerializerWithToken
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
     def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getUserProfile(request):
    user=request.user

    serializer= UserSerializer(user,many=False)

    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        client= Client.objects.create(
            user=user,
            telephone=data['tel'],
            infos_liv=data['infos_liv']
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User avec ce email deja exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifierUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data = request.data
    try:
      user.first_name = data['name']
      user.username = data['email']
      user.email = data['email']
      if user.is_staff==False:
        client=Client.objects.get(user=user)
        client.telephone=data['tel']
        client.infos_liv=data['infos_liv']
        client.save()

      if data['password'] != '':
            user.password = make_password(data['password'])

      user.save()
    except:
        return Response({'detail':'Email a changé deja existe'},status = status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    try:
        user = User.objects.get(id=int(pk))
        serializer = UserSerializer(user, many=False)
    except:
        return Response({'detail':'utilisateur inexistant'},status = status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def supprimerUser(request, pk):
    try:
        user = User.objects.get(id=int(pk))
        user.delete()
    except:
        return Response({'detail':'utilisateur inexistant'},status = status.HTTP_400_BAD_REQUEST)
    return Response('utilisateur est supprimé')