from django.urls import path
from store.views import categorie_views as views

urlpatterns = [
        path('',views.CategorieParent.as_view(),name='home'),
        path('<str:catP_id>/',views.CategorieFilsList.as_view(),name='cat_fils'),
        path('catFil/<str:catF_id>',views.ProduitCat.as_view(),name='produit_cat'),
        path('aj/ajouter/',views.ajouterCategorie.as_view(),name='ajouter_cat'),
        path('aj/modifier/<str:pk>',views.modifierCategorie.as_view(),name='modifier_cat'),
        
        ]