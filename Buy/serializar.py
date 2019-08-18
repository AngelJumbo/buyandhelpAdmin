from .models import *
from rest_framework import serializers

class ArticuloSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articulo
        fields = '__all__'

class RolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class EstadoPedidoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EstadoPedido
        fields = '__all__'

class PedidoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class ArticuloPedidoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articulo
        fields = '__all__'

class TipoPagoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoPago
        fields = '__all__'

class PagoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class PublicacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class PuntuacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'