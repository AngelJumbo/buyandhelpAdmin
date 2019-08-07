from .models import Articulo
from rest_framework import serializers

class DawSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articulo
        fields = ('id_articulo','nombre','precio','donacion','descrip')