from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
    tel=serializers.SerializerMethodField(read_only=True)
    infosliv=serializers.SerializerMethodField(read_only=True)


    class Meta:
        model=User 
        fields=['id','username','email','name','isAdmin','tel','infosliv']
    def get_name(self,obj):
        name=obj.first_name
        if name == '':
            name=obj.email
        return name 

    def get_isAdmin(self,obj):
        return obj.is_staff
    
    def get_tel(self,obj):
        if obj.is_staff==False:
            client=Client.objects.get(user=obj)
            tel=client.telephone
        else:
            tel=''        
        return tel
    def get_infosliv(self,obj):
        if obj.is_staff==False:
            client=Client.objects.get(user=obj)
            tel=client.infos_liv
        else:
            tel=''        
        return tel

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin','tel','infosliv', 'token',]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields='__all__'

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model=Produit
        fields='__all__'
    

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categorie
        fields='__all__'

class ContactSerializer(serializers.ModelSerializer):
    tel=serializers.SerializerMethodField(read_only=True)
    email=serializers.SerializerMethodField(read_only=True)
    nom=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=Contact
        fields=['id','nom','email', 'tel', 'sujet','message']

    def get_tel(self,obj):
        user=obj.emetteur
        if user.first_name!='visiteur' and user.is_staff==False:
            tel=user.clients.telephone

        else:
            if user.is_staff==True:
                tel=''
            else:
                contact=ContactVisiteur.objects.get(base=obj)
                tel=contact.tel
        return (tel)
    
    def get_email(self,obj):
        user=obj.emetteur
        if user.first_name!='visiteur':
            email=user.email
        else:
            contact=ContactVisiteur.objects.get(base=obj)
            email=contact.email
        return (email)

    def get_nom(self,obj):
        user=obj.emetteur
        if user.first_name!='visiteur':
            nom=user.first_name
        else:
            contact=ContactVisiteur.objects.get(base=obj)
            nom=contact.nom
        return (nom)
        
class ContactVisiteurSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactVisiteur
        fields='__all__'

class LigneCmdSerializer(serializers.ModelSerializer):
    class Meta:
        model=LigneCmd
        fields='__all__'
class CommandeSerializer(serializers.ModelSerializer):
    lignecmds = LigneCmdSerializer(many=True,read_only=True)

    class Meta:
        model=Commande
        fields='__all__'

    