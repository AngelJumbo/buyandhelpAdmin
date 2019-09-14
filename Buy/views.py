from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .forms import ContactForm
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status, viewsets
from django.http import HttpResponse
from .models import Usuario as UsuarioModel
from .models import Imagen
from base64 import b64decode
from django.core.files.base import ContentFile
from django.contrib import auth


# Create your views here.
#index

def index1(request):
    return render(request, "index.html")

def apis(request):
    return render(request, "apis.html")

def handler404(request, exception):
    data = {}
    return render(request, '404.html', data)

#formulario contactenos

class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()

        return context
        

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        city = request.POST.get('city')
        email = request.POST.get('email')
        issue = request.POST.get('issue')
        message = request.POST.get('message')

        body = render_to_string(
            'email_content.html', {
                'name': name,
                'city': city,
                'email': email,
                'issue': issue,
                'message': message,
            },
        )

        email_message = EmailMessage(
            subject='Mensaje de usuario',
            body=body,
            from_email='milton.garcia1998@hotmail.com',
            to=['milton.garcia1998@hotmail.com','adanavarrete15@gmail.com'],
        )
        email_message.content_subtype = 'html'
        email_message.send()


        return redirect('contact')

# Serializer OK
class ImagenesList(generics.ListCreateAPIView):
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer

# Serializer OK
class ImagenesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer


# Serializer OK
class ArticulosList(generics.ListCreateAPIView):

    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    def list(self, request, *args, **kwargs):
        queryset = Articulo.objects.all()
        serializer = ArticuloSerializerDetail(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = ArticuloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# Serializer OK
class ArticulosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer

    def retrieve(self, request, pk):
        try:
            articulo = Articulo.objects.get(pk=pk)
            serializer = ArticuloSerializerDetail(articulo, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Articulo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        try:
            articulo = Articulo.objects.get(pk=pk)
            serializer = ArticuloSerializer(articulo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Articulo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Serializer OK
class UsuariosViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        queryset = UsuarioModel.objects.all()
        serializer = UsuarioSerializerDetail(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, requset, pk):
        try:
            usuario = UsuarioModel.objects.get(pk=pk)
            serializer = UsuarioSerializerDetail(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UsuarioModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        try:
            usuario = UsuarioModel.objects.get(pk=pk)
            usuario.delete()
        except UsuarioModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Serializer OK
class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk = self.kwargs['pk'],
        )

        return obj


# Serializer OK
class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


#get, post
class PedidoList(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk = self.kwargs['pk'],
        )

        return obj

#updtate, delete
class PedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


#get, post
class ArticuloPedidoList(generics.ListCreateAPIView):
    queryset = ArticuloPedido.objects.all()
    serializer_class = ArticuloPedidoSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk = self.kwargs['pk'],
        )

        return obj

#updtate, delete
class ArticuloPedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticuloPedido.objects.all()
    serializer_class = ArticuloPedidoSerializer


#get, post
class PagoList(generics.ListCreateAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk = self.kwargs['pk'],
        )

        return obj

#updtate, delete
class PagoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer


#get, post
class PublicacionList(generics.ListCreateAPIView):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk = self.kwargs['pk'],
        )

        return obj


#updtate, delete
class PublicacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer


#get, post
class PuntuacionVendedorList(generics.ListCreateAPIView):
    queryset = PuntuacionVendedor.objects.all()
    serializer_class = PuntuacionSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk = self.kwargs['pk'],
        )

        return obj


#updtate, delete
class PuntuacionVendedorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PuntuacionVendedor.objects.all()
    serializer_class = PuntuacionSerializer



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Usuario(APIView):
    def get(self, request):
        usuarios = UsuarioModel.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self,request):
        UsuarioModel.objects.create(
            rol=request.data.get('rol'),
            cedula=request.data.get('cedula'),
            contrasenia=request.data.get('contrasenia'),
            nombres=request.data.get('nombres'),
            apellidos=request.data.get('apellidos'),
            email=request.data.get('email'),
            direccion=request.data.get('direccion'))
        return HttpResponse(status=201)


class CategoriaList2(APIView):
    def get(self, request):
        categorias=Categoria.objects.all()
        serializer=CategoriaSerializer(categorias,many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ArticuloList(APIView):
    def get(self, request):
        articulos=Articulo.objects.all()
        #imagenes=Imagen.objects.all()
        serializer=ArticuloSerializer(articulos,many=True)
        return Response(serializer.data)

    def post(self,request):
        pass

class ArticuloListComprador(APIView):

    def get_object(self, pk):
        try:
            return Articulo.objects.get(pk=pk)
        except Articulo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        articulos=Articulo.objects.filter(usuario__id=request.GET['id_usuario'])
        serializer=ArticuloSerializerDetail(articulos,many=True,context={'request':request})
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            articulo=Articulo.objects.get(pk=pk)
            articulo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Articulo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class buscarUsuario(APIView):
    def get(self, request):
        usuario = UsuarioModel.objects.get(cedula=request.GET['cedula'])
        serialized_obj = UsuarioSerializer(usuario, many=False)
        #serialized_obj = serializers.serialize('json', [ usuario, ])
        #dict_obj = model_to_dict( usuario )
        #serialized_obj = json.dumps(dict_obj)
        
        #return HttpResponse(serialized_obj, mimetype='application/json')
        return Response(serialized_obj.data)

class comprobarUsuario(APIView):
    def post(self,request):

        username = request.data.get('username')
        password = request.data.get('password')

        print(username, password)
        user = auth.authenticate(username=username, password=password)
        print(user)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                serializer = UsuarioSerializerDetail(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)