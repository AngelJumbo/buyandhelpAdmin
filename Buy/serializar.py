from .models import *
from rest_framework import serializers

class ImagenSerializer(serializers.ModelSerializer):
    imagen=serializers.ImageField(
            max_length=None, use_url=True
        )
    class Meta:
        model = Imagen
        fields = ('id_imagen','id_articulo','imagen')
    
    

class ArticuloSerializer2(serializers.ModelSerializer):    
    imagenes = ImagenSerializer(many=True, read_only=True)      
    class Meta:        
        model = Articulo         
        fields = ('id_articulo','id_categoria','id_usuario','nombre','precio','donacion','descrip','imagenes')


class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPedido
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class ArticuloPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloPedido
        fields = '__all__'

class TipoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'

class PuntuacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntuacionVendedor
        fields = '__all__'