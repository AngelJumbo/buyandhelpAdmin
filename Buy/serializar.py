from .models import Articulo
from rest_framework import serializers

class ArticuloSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articulo
        fields = ('id_articulo','id_categoria','id_usuario','nombre','precio','donacion','descrip')