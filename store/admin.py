from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Client)
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Contact)
admin.site.register(ContactVisiteur)
admin.site.register(Commande)
admin.site.register(LigneCmd)