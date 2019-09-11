from .models import *
from rest_framework import serializers
from .models import Usuario

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
        fields = ('categoria','usuario','nombre','precio','donacion','descrip','imagenes')


class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = '__all__'


class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = ('rol', 'cedula', 'direccion')


class UsuarioSerializer(serializers.ModelSerializer):

    perfil = PerfilSerializer(required=True, write_only=True)
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password', 'perfil')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        perfil = validated_data.pop('perfil')
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        Perfil.objects.create(usuario=user, **perfil)
        return user


class UsuarioSerializerDetail(serializers.HyperlinkedModelSerializer):

    perfil = PerfilSerializer()
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'username', 'perfil')


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class ArticuloPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloPedido
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