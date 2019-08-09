from django.urls import path
from .views import index1
from django.conf.urls import url
from .views import *


urlpatterns = [
    path('', index1, name="index"),
    url(r'^articulos/$',ArticulosList.as_view(), name ='articulos'),
    url(r'^pizzerias/(?P<pk>[0-9]+)/$', ArticulosDetail.as_view()),
]