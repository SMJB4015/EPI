from django.shortcuts import render
from store.serializers import ProduitSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from store.models import Produit,Categorie
from django.shortcuts import render,get_object_or_404
from rest_framework import status
from datetime import datetime


@api_view(['GET'])
def getProduits(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    produits = Produit.objects.filter(
        nom__icontains=query).order_by('-date_creation')

    page = request.query_params.get('page')
    paginator = Paginator(produits, 5)

    try:
        produits = paginator.page(page)
    except PageNotAnInteger:
        produits = paginator.page(1)
    except EmptyPage:
        produits = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ProduitSerializer(produits, many=True)
    return Response({'produits': serializer.data, 'page': page, 'pages': paginator.num_pages})
class ProduitDetails(APIView):
    def get(self,request,pk):
        produit=get_object_or_404(Produit,pk=int(pk))
        data=ProduitSerializer(produit).data
        return Response(data)


class Promo(APIView):
    def get(self,request):
       
        produits=Produit.objects.filter(promotion=True)

        page = request.query_params.get('page')
        paginator = Paginator(produits, 5)

        try:
            produits = paginator.page(page)
        except PageNotAnInteger:
            produits = paginator.page(1)
        except EmptyPage:
            produits = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        print('Page:', page)
        serializer = ProduitSerializer(produits, many=True)
        return Response({'produits': serializer.data, 'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
def getNouveau(request):
    produits = Produit.objects.all().order_by('-date_creation')[0:5]
    serializer = ProduitSerializer(produits, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def ajouterProduit(request):
    data=request.data
    categorie=Categorie.objects.get(name=data['categorie'])
    produit = Produit.objects.create(
        nom=data['nom'],
        ref=data['ref'],
        description=data['description'],
        categorie=categorie ,
        marque=data['marque'],
        tva=data['tva'],
        promotion=data['promotion'],
        prix=data['prix'],
        prix_promo=data['prix_promo'],
        commentaire=data['commentaire'],
        
    )

    serializer = ProduitSerializer(produit, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def modifierProduit(request, pk):
    data = request.data

    produit = Produit.objects.get(id=str(pk))
    serializer = ProduitSerializer(produit, data=data)

    if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def supprimerProduit(request, pk):
    produit = Produit.objects.get(id=int(pk))
    produit.delete()
    return Response('Produit Supprimé')

@api_view(['POST'])
def uploadImage(request):
    data = request.data

    produit_id = data['id']
    produit = Produit.objects.get(id=int(produit_id))

    produit.image = request.FILES.get('image')
    produit.save()

    return Response('Image was uploaded')