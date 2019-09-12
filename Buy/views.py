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


class ImagenesList(generics.ListCreateAPIView):

    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer


class ImagenesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer


#API REST
#get, post
class ArticulosList(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        queryset = Articulo.objects.all()
        serializer = ArticuloSerializerDetail(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = ArticuloSerializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


#updtate, delete
class ArticulosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializerDetail


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


#get, post
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

#updtate, delete
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
        articulos=Articulo.objects.filter(id_usuario=request.GET['id_usuario'])
        serializer=ArticuloSerializer(articulos,many=True)
        return Response(serializer.data)

    def post(self,request):
        
        print("post !!!!!!!!!!!", flush=True)
        if(Articulo.objects.filter(id_articulo=request.data.get('id_articulo')).exists()):
            print("post2 !!!!!!!!!!!", flush=True)
            articulo=Articulo.objects.get(id_articulo=request.data.get('id_articulo'))
            print("post2 !!!!!!!!!!!", flush=True)
            articulo.id_categoria=Categoria.objects.get(id_categoria=request.data.get('id_categoria'))
            print("post2 !!!!!!!!!!!", flush=True)
            articulo.nombre=request.data.get('nombre')
            print("post2 !!!!!!!!!!!", flush=True)
            articulo.precio=request.data.get('precio')
            print("post2 !!!!!!!!!!!", flush=True)
            articulo.donacion=request.data.get('donacion')
            articulo.descrip=request.data.get('descrip')
            articulo.save()

            if(not (request.data.get('imagen') is None)):
                imagenAnterior=Imagen.objects.get(id_articulo=articulo.id_articulo)
                imagenAnterior.delete()
                imagenArchi=b64decode(request.data.get('imagen'))
                Imagen.objects.create(
                    id_articulo=articulo,
                    imagen=ContentFile(imagenArchi,request.data.get('imagen_nombre')))

                return HttpResponse(status=201)


        else:
            articulo=Articulo.objects.create(
                id_usuario=UsuarioModel.objects.get(id_usuario=request.data.get('id_usuario')),
                id_categoria=Categoria.objects.get(id_categoria=request.data.get('id_categoria')),
                nombre=request.data.get('nombre'),
                precio=request.data.get('precio'),
                donacion=request.data.get('donacion'),
                descrip=request.data.get('descrip'))
            imagenArchi=b64decode(request.data.get('imagen'))
            Imagen.objects.create(
                id_articulo=articulo,
                imagen=ContentFile(imagenArchi,request.data.get('imagen_nombre')))

            return HttpResponse(status=201)

    def delete(self, request):

        articulo=Articulo.objects.get(id_articulo=request.GET['id_articulo'])
        articulo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

        #request.data.get('id_rol')
        usuario=UsuarioModel.objects.get(cedula=request.data.get('cedula'),contrasenia=request.data.get('contrasenia'))
        serialized_obj = UsuarioSerializer(usuario, many=False)

        return Response(serialized_obj.data)
