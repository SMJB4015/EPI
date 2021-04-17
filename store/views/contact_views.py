from django.shortcuts import render
from store.serializers import ContactSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from store.models import Contact,ContactVisiteur
from rest_framework import status
from django.contrib.auth.models import User
from datetime import datetime


@api_view(['POST'])
def createMessage(request):
    user=request.user
    admin=User.objects.get(is_staff=True)
    if request.user.is_anonymous:
        user=User.objects.get(first_name='visiteur')
        contact=Contact.objects.create(
            message=request.data['message'],
            sujet=request.data['sujet'],
            emetteur=user,
            recepteur=admin
        )
        contactVis=ContactVisiteur.objects.create(
            base=contact,
            email=request.data['email'],
            nom=request.data['nom'],
            prenom=request.data['prenom'],
            tel=request.data['tel']
        )
        return Response({'detail':'Votre Message a etait envoyé à la administration'})
    else:
        if request.user.is_staff:
            user=User.objects.get(id=request.data['recp'])
            contact=Contact.objects.create(
            message=request.data['message'],
            sujet=request.data['sujet'],
            emetteur=admin,
            recepteur=user
            )
            return Response({"detail":"Message envoyé"})

        else:
            contact=Contact.objects.create(
            message=request.data['message'],
            sujet=request.data['sujet'],
            emetteur=user,
            recepteur=admin
            )
        return Response({'detail':'Cher client Votre Message a etait envoyé à la administration'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def boiteMessage(request):
    user=request.user
    contact=Contact.objects.filter(recepteur=user).all()
    if len(contact)==0:
        return Response({"detail": "Vous n'avez pas des messages" })
    serializer=ContactSerializer(contact,many=True)
    return Response(serializer.data)

