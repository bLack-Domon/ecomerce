from django.urls import path
from .import views


urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('profil', views.profil, name='profil'),
    path('<slug:kategori_slug>/<slug:slug>', views.product, name='product'),
    path('kontak', views.KontakView.as_view(), name='kontak'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('cari', views.cari, name='cari'),
    path('<slug:slug>', views.kategori, name='kategori'),
  
  
]
