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
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Create your views here.
#index

def index1(request):
    return render(request, "index.html")

def apis(request):
    return render(request, "apis.html")

def handler404(request, exception):
    data = {}
    return render(request, '404.html', data)

class ContactEmail(APIView):

    def post(self, request):
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

        message = Mail(
            from_email=settings.EMAIL_HOST_USER,
            to_emails='cindy9319@gmail.com',
            subject='CORREO DAW',
            html_content=body)
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e.message)
            return Response(status=status.HTTP_400_BAD_REQUEST)


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

        print(body)
        subject = 'Contacto'
        message = body
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['geanleto@gmail.com',]
        if send_mail(subject, message, email_from, recipient_list):
            print('OK')
        else:
            print(":(")
        '''
        email_message = EmailMessage(
            subject='Mensaje de usuario',
            body=body,
            from_email='pruebadjangomail@gmail.com',
            to=['milton.garcia1998@hotmail.com','adanavarrete15@gmail.com', 'pruebadjangomail@gmail.com'],
        )
        email_message.content_subtype = 'html'
        email_message.send()
        '''

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


class LikeArticule(APIView):

    def post(self, request, pk):
        try:
            articulo = Articulo.objects.get(pk=pk)
            data = request.data
            if 'user' not in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            usuario = UsuarioModel.objects.get(pk=data['user'])
            if data['user'] not in articulo.liked_by.values_list(flat=True):
                articulo.liked_by.add(usuario)
                articulo.likes = articulo.liked_by.count()
                articulo.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Articulo.DoesNotExist or UsuarioModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DislikeArticulo(APIView):

    def post(self, request, pk):
        try:
            articulo = Articulo.objects.get(pk=pk)
            data = request.data
            if 'user' not in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            usuario = UsuarioModel.objects.get(pk=data['user'])
            if data['user'] in articulo.liked_by.values_list(flat=True):
                articulo.liked_by.remove(usuario)
                articulo.likes = articulo.liked_by.count()
                articulo.save()
                return Response(status=status.HTTP_200_OK)
            print('ultimo', data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Articulo.DoesNotExist or UsuarioModel.DoesNotExist:
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


class CarritoList(generics.ListAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializerDetail


class CarritoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    def retrieve(self, request, pk):
        try:
            carrito = Carrito.objects.get(usuario__id=pk)
            serializer = CarritoSerializerDetail(carrito, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Carrito.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk):
        try:
            carrito = Carrito.objects.get(usuario__id=pk)
            serializer = CarritoSerializer(carrito, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Carrito.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeCarritoAPedido(APIView):

    def post(self, request, pk):
        try:
            carrito = Carrito.objects.get(usuario__id=pk)
            articulos = Articulo.objects.filter(carrito=carrito)
            print(articulos)
            if len(articulos) > 0:
                suma = Articulo.objects.filter(carrito=carrito).aggregate(Sum('precio'))
                print(suma)
                pedido = Pedido.objects.create(comprador=carrito.usuario, total_venta=suma['precio__sum'])
                for articulo in articulos:
                    ArticuloPedido.objects.create(pedido=pedido, articulo=articulo)
                carrito.articulos.clear()
                return Response(status=status.HTTP_200_OK)
            return Response({'error': 'Carrito Vacio'}, status=status.HTTP_404_NOT_FOUND)
        except Carrito.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


#get, post
class PedidoList(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def list(self, request, *args, **kwargs):
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializerDetail(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#updtate, delete
class PedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def retrieve(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk)
            serializer = PedidoSerializerDetail(pedido)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Pedido.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


#get, post
class ArticuloPedidoList(generics.ListCreateAPIView):
    queryset = ArticuloPedido.objects.all()
    serializer_class = ArticuloPedidoSerializer

    def list(self, request, *args, **kwargs):
        articulopedido = ArticuloPedido.objects.all()
        serializer = ArticuloPedidoSerializerDetail(articulopedido, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


#updtate, delete
class ArticuloPedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticuloPedido.objects.all()
    serializer_class = ArticuloPedidoSerializer

    def retrieve(self, request, pk):
        try:
            artped = ArticuloPedido.objects.get(pk=pk)
            serializer = ArticuloPedidoSerializerDetail(artped, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ArticuloPedido.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


#get, post
class PagoList(generics.ListCreateAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

    def list(self, request, *args, **kwargs):
        pagos = Pago.objects.all()
        serializer = PagoSerializerDetail(pagos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#updtate, delete
class PagoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

    def retrieve(self, request, pk):
        try:
            pago = Pago.objects.get(pk=pk)
            serializer = PagoSerializerDetail(pago)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Pago.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


class EstadisticaPedidos(APIView):

    def get(self, request, pk):
        try:
            pedidos = Pedido.objects.filter(comprador_id=pk)
            pedido_serializer = PedidoSerializerDetail(pedidos, many=True)
            suma = Pedido.objects.filter(comprador_id=pk).aggregate(Sum('total_venta'))
            data = {'data': pedido_serializer.data, 'total': suma['total_venta__sum']}
            return Response(data, status=status.HTTP_200_OK)
        except Pedido.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EstadisticaPagos(APIView):

    def get(self, request, pk):
        try:
            pagos = Pago.objects.filter(pedido__comprador__id=pk)
            pagos_serializer = PagoSerializerDetail(pagos, many=True)
            suma = Pago.objects.filter(pedido__comprador__id=pk).aggregate(Sum('pedido__total_venta'))
            print(suma)
            # pedido_serializer = PedidoSerializerDetail(pedidos, many=True)
            # suma = Pedido.objects.filter(comprador_id=pk).aggregate(Sum('total_venta'))
            # data = {'data': pedido_serializer.data, 'total': suma['total_venta__sum']}
            return Response(pagos_serializer.data, status=status.HTTP_200_OK)
        except Pedido.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


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


class usuariosPorTipo(APIView):

    def get(self, request):
        vendedores = Perfil.objects.filter(rol='VEN').count()
        compradores = Perfil.objects.filter(rol='COM').count()
        admins = Perfil.objects.filter(rol='ADM').count()
        return Response(data=[
            {
                'name': 'Vendedores',
                'value': vendedores
            },
            {
                'name': 'Compradores',
                'value': compradores
            },
            {
                'name': 'Administradores',
                'value': admins
            }
        ], status=status.HTTP_200_OK)


class estadisticasPedidos(APIView):

    def get(self, request):
        cantidad = []
        suma_data = []
        categorias = Categoria.objects.all()
        for categoria in categorias:
            n = ArticuloPedido.objects.filter(articulo__categoria=categoria).count()
            suma = ArticuloPedido.objects.filter(articulo__categoria=categoria).aggregate(Sum('articulo__precio'))
            cantidad.append({'name': categoria.nombre, 'value': n})
            if suma['articulo__precio__sum']:
                suma_data.append({'name': categoria.nombre, 'value': suma['articulo__precio__sum']})
            else:
                suma_data.append({'name': categoria.nombre, 'value': 0})
        return Response(data={'cantidad': cantidad, 'suma': suma_data}, status=status.HTTP_200_OK)