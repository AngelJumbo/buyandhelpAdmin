"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path,include
from django.conf import settings
#from rest_framework.authtoken import views

from django.views.generic.base import RedirectView
#!!
from rest_framework.urlpatterns import format_suffix_patterns
from Buy import views
from django.conf.urls.static import static


urlpatterns = [
    path('api/', include('Buy.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='api/', permanent=False), name="index"),
    #url('django-sb-admin/', include('django_sb_admin.urls')),
    #!!!!!!!!!!!!!!!!!!!!!!!!!
    path('categorias/', views.CategoriaList2.as_view()),
    path('todosLosArticulos/', views.ArticuloList.as_view()),
    path('articulosComprador/', views.ArticuloListComprador.as_view()),
    path('articulosComprador/<int:pk>/', views.ArticuloListComprador.as_view()),
    path('usuario/', views.Usuario.as_view()),
    path('usuario/<int:pk>/', views.Usuario.as_view()),
    path('buscarUsuario/', views.buscarUsuario.as_view()),
    path('buscarUsuario/<int:pk>/', views.buscarUsuario.as_view()),
    path('comprobarUsuario/', views.comprobarUsuario.as_view()),
    path('comprobarUsuario/<int:pk>/', views.comprobarUsuario.as_view()),
    # path('imagenes/', views.imagenes.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Habilitar carpeta imagenes
