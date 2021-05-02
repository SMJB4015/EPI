from django.shortcuts import render,get_object_or_404
from store.models import *
from django.http import JsonResponse
from store.serializers import ClientSerializer, ProduitSerializer,  CategorieSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser




# Create your views here.

@permission_classes([IsAdminUser])
class ajouterCategorie(APIView):

    def post(self,request):
        data=request.data
        if data['categorie']!='':
            cat=Categorie.objects.get(name=data['categorie'])
        else:
                cat=None

        categorie = Categorie.objects.create(
            name=data['name'],
            description=data['description'],
            parent=cat,
        )

        serializer = CategorieSerializer(categorie, many=False)
        return Response(serializer.data)
        
@permission_classes([IsAdminUser])
class modifierCategorie(APIView):
    def put(self,request,pk):
        data=request.data
        categorie=Categorie.objects.get(id=int(pk))
        if data['categorie']!='':
            cat=Categorie.objects.get(name=data['categorie'])
        else:
                cat=None
        categorie.name=data['name']
        categorie.description=data['description']
        categorie.parent=cat
        categorie.save()
        serializer = CategorieSerializer(categorie, many=False)
        return Response(serializer.data)

class CategorieParent(generics.ListAPIView):
    queryset = Categorie.objects.filter(parent=None)
    serializer_class = CategorieSerializer


class CategorieFilsList(APIView):
    def get(self,request,catP_id):
        cat=get_object_or_404(Categorie,pk=int(catP_id))
        fils=Categorie.objects.filter(parent=cat.id)
        data= CategorieSerializer(fils,many=True).data
        return Response(data)

class ProduitCat(APIView):
    def get(self,request,catF_id):
       
        cat = get_object_or_404(Categorie, pk=int(catF_id))
        produits=Produit.objects.filter(categorie=cat.id)

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

class ProduitCatM(APIView):
    def get(self,request,catF_id):
       
        cat = get_object_or_404(Categorie, pk=int(catF_id))
        produits=Produit.objects.filter(categorie=cat.id)
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)



