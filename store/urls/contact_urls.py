from django.urls import path
from store.views import contact_views as views

urlpatterns = [
    path('creation/',views.createMessage,name='creation_message') ,
    path('boite/',views.boiteMessage,name='boite_message')


]