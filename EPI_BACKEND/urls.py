from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/client/', include('store.urls.client_urls')),
    path('api/categorie/', include('store.urls.categorie_urls')),
    path('api/commande/', include('store.urls.commande_urls')),
    path('api/produit/', include('store.urls.produit_urls')),
    path('api/contact/', include('store.urls.contact_urls')),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)