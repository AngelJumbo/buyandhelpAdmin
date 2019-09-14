from .models import *
from rest_framework import serializers
from .models import Usuario


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
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


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ImagenSerializer(serializers.ModelSerializer):
    imagen=serializers.ImageField(
            max_length=None, use_url=True
        )
    class Meta:
        model = Imagen
        fields = ('id','imagen','articulo','url')


class ImagenCreateSerializer(serializers.ModelSerializer):
    imagen=Base64ImageField(
            max_length=None, use_url=True
        )
    class Meta:
        model = Imagen
        fields = ('imagen',)


class ArticuloSerializer(serializers.ModelSerializer):

    imagen = ImagenCreateSerializer(write_only=True)
    class Meta:
        model = Articulo
        fields = ('id', 'categoria','usuario','nombre','precio','donacion','descrip', 'imagen')

    def create(self, validated_data):
        imagenes = validated_data.pop('imagen')
        articulo = Articulo(**validated_data)
        articulo.save()
        for imagen in imagenes.values():
            print(imagen)
            Imagen.objects.create(articulo=articulo, imagen=imagen)
        return articulo


class ArticuloSerializerList(serializers.ModelSerializer):

    categoria = CategoriaSerializer()
    usuario = UsuarioSerializerDetail()
    class Meta:
        model = Articulo
        fields = ('id', 'categoria','usuario','nombre','precio','donacion','descrip')


class ArticuloSerializerDetail(serializers.ModelSerializer):

    imagenes = ImagenSerializer(many=True)
    categoria = CategoriaSerializer(read_only=True)
    usuario = UsuarioSerializerDetail(read_only=True)
    class Meta:        
        model = Articulo         
        fields = ('id', 'categoria','usuario','nombre','precio','donacion','descrip','imagenes')


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