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
        if  perfil['rol'] == 'COM':
            Carrito.objects.create(usuario=user)
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
            Imagen.objects.create(articulo=articulo, imagen=imagen)
        return articulo

    def update(self, instance, validated_data):
        imagenes = validated_data.pop('imagen') if validated_data.get('imagen') else []
        instance.categoria = validated_data.pop('categoria') if validated_data.get('categoria') else instance.categoria
        instance.usuario = validated_data.pop('usuario') if validated_data.get('usuario') else instance.usuario
        instance.nombre = validated_data.pop('nombre') if validated_data.get('nombre') else instance.nombre
        instance.precio = validated_data.pop('precio') if validated_data.get('precio') else instance.precio
        instance.donacion = validated_data.pop('donacion') if validated_data.get('donacion') else instance.donacion
        instance.descrip = validated_data.pop('descrip') if validated_data.get('descrip') else instance.descrip
        instance.save()
        if len(imagenes) > 0:
            Imagen.objects.filter(articulo__id=instance.id).delete()
            for imagen in imagenes.values():
                Imagen.objects.create(articulo=instance, imagen=imagen)
        return instance


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


class ArticuloSerializerDetailSinImagen(serializers.ModelSerializer):

    categoria = CategoriaSerializer(read_only=True)
    usuario = UsuarioSerializerDetail(read_only=True)
    class Meta:
        model = Articulo
        fields = ('id', 'categoria','usuario','nombre','precio','donacion','descrip')


class CarritoSerializerDetail(serializers.ModelSerializer):

    usuario = UsuarioSerializerDetail()
    articulos = ArticuloSerializerDetail(many=True)
    class Meta:
        model = Carrito
        fields = ('id', 'usuario', 'articulos')


class CarritoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carrito
        fields = ('id', 'usuario', 'articulos')


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class PedidoSerializerDetail(serializers.ModelSerializer):

    articulos = serializers.SerializerMethodField()
    comprador = UsuarioSerializerDetail()
    class Meta:
        model = Pedido
        fields = ('id', 'estado_pedido', 'fecha', 'total_venta', 'comprador', 'articulos')

    def get_articulos(self, object):
        articulos = ArticuloPedido.objects.filter(pedido=object).values_list('articulo', flat=True)
        qs = Articulo.objects.filter(id__in=articulos)
        return ArticuloSerializerDetailSinImagen(qs, many=True).data


class ArticuloPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloPedido
        fields = '__all__'


class ArticuloPedidoSerializerDetail(serializers.ModelSerializer):

    articulo = ArticuloSerializerDetail()
    pedido = PedidoSerializerDetail()
    class Meta:
        model = ArticuloPedido
        fields = ('id', 'articulo', 'pedido')


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