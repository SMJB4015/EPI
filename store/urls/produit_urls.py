from django.urls import path
from store.views import produit_views as views

urlpatterns = [
     path('', views.getProduits, name="produits"),
     path('detail/<str:pk>/',views.ProduitDetails.as_view(),name='produit_dt'),
     path('promotion/',views.Promo.as_view(),name='promo'),
     path('nouveau/', views.getNouveau, name="produits_nouveau"),
     path('ajouter/', views.ajouterProduit, name="produits_ajouter"),
     path('modifier/<str:pk>/', views.modifierProduit, name="produits_modifer"),
     path('supprimer/<str:pk>/', views.supprimerProduit, name="produits_supprimer"),
     path('upload/', views.uploadImage, name="image-upload"),







]
