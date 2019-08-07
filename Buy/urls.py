from django.urls import path
from .views import index1
from django.conf.urls import url
from .views import *


urlpatterns = [
    path('', index1, name="index"),
    url(r'^Buy/$',DawList.as_view(), name ='Buy')
]