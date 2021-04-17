from django.urls import path
from store.views import commande_views as views

urlpatterns = [
        path('',views.getCommandes,name='commandes'),
        path('ajouter/',views.ajouterLigneCmd,name='ajouter-commande'),
        path('commande_details/<str:pk>/',views.getCommandeById,name='commandeDetail'),
        path('verifier/<str:pk>/',views.verifCommande,name='verifier-commande'),
        path('mescommandes/',views.getMesCommandes,name='mes-commandes'),
        path('modifier/<str:pk>/',views.modifierCommande,name='modifier_commande'),
        path('supprimer/<str:pk>/',views.supprimerCommande,name='supprimer_commande'),

        
        ]