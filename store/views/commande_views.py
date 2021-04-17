from django.shortcuts import render
from store.serializers import CommandeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from store.models import Commande,LigneCmd,Produit,Client
from rest_framework import status
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ajouterLigneCmd(request):
    user=request.user
    data=request.data
    
    lignesPan=data['lignesPan']
    

    if (len(lignesPan) == 0):
        return Response({'detail': "Il n'ya pas des Lignes de Commande"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        commande=Commande.objects.create(
            client=user,
            etat='N',
            modification=False,
            infos_liv=data['infos_liv'],
            totalHT=data['totalHT'],
            totaltTTC=data['totalTTC']

        )

        for i in lignesPan:
            produit = Produit.objects.get(id=i['produit'])

            ligne=LigneCmd.objects.create(
                produit=produit,
                commande=commande,
                qte=i['qte'],
            )
    
    serializer=CommandeSerializer(commande,many=False)
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getCommandes(request):
    commandes = Commande.objects.all()
    serializer = CommandeSerializer(commandes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMesCommandes(request):
    user=request.user
    try:
        commandes = user.commandes_set.all()
    except:
        return Response({'details':'Pas de commandes pour ce utilisateur'}, status = status.HTTP_400_BAD_REQUEST)

    serializer = CommandeSerializer(commandes,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCommandeById(request, pk):

    user = request.user
    try:
        commande = Commande.objects.get(id=int(pk))
        if user.is_staff or commande.user == user:
            if (user.is_staff) and (commande.etat == 'N'):
                    commande.etat='E'
                    commande.save()

            serializer = CommandeSerializer(commande, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Non autorisé pour consulter ce commande'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"detail": "Cette commande n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def verifCommande(request, pk):
    commande = Commande.objects.get(id=int(pk))

    commande.etat = "V"
    commande.save()

    return Response('Commande est verifié')

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifierCommande(request, pk):
    user=request.user
    try:
        commande = Commande.objects.get(id=int(pk))
        if  (commande.user == user) and (commande.etat!='V'):
            lignesCmd=data['lignesCmd']
            if lignesCmd and len(lignesCmd) == 0:
                commande.delete()
                return Response({'detail': "La Commande est Supprimé"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                lignes=Commande.lignescmds_set.all()
                for i in lignes:
                    i.delete()
                for j in lignesCmd:
                    produit = Produit.objects.get(id=j['produit'])
                    ligne=LigneCmd.objects.create(
                        produit=produit,
                        commande=commande,
                        qte=j['qte'],
                    )
                commande.modification=True
                commande.date_modi=datetime.now()
                commande.save()

                serializer = CommandeSerializer(commande, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': ' Utilisateur Non autorisé pour consulter ce commande Ou Commande Deja verifié'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"detail": "Cette commande n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimerCommande(request, pk):
    user=request.user
    try:
        commande = Commande.objects.get(id=int(pk))
        if  ((commande.user == user) and (commande.etat!='V')) or (user.is_staff):
            commande.delete()
            return Response({'detail': "La Commande est Supprimé"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response({'detail': ' Utilisateur Non autorisé pour Supprimer ce commande Ou Commande Deja verifié'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"detail": "Cette commande n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)


