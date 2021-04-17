from django.urls import path
from store.views import client_views as views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.getUserProfile, name='client_profile'),
    path('register/', views.registerUser, name='client_register'),
    path('modifier/', views.modifierUserProfile, name='client_modifier'),
    path('', views.getUsers, name='client_list'),
    path('<str:pk>', views.getUserById, name='client_par_id'),
    path('supprimer/<str:pk>', views.supprimerUser, name='client_supprimer'),



]

    
