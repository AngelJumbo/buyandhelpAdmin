from django.urls import path
from .views import index1
from django.conf.urls import url
from .views import *
from django.conf.urls import handler404


urlpatterns = [
    path('', index1, name='index'),

    # Articulos OK
    path('articulos/',ArticulosList.as_view(), name ='articulos'),
    path('articulos/<int:pk>/', ArticulosDetail.as_view()),
    path('like/<int:pk>/', LikeArticule.as_view()),
    path('dislike/<int:pk>/', DislikeArticulo.as_view()),

    # Imagenes OK
    path('imagenes/', ImagenesList.as_view(), name='imagenes-list'),
    path('imagenes/<int:pk>/', ImagenesDetail.as_view(), name='imagen-detail'),

    # Usuarios OK
    path('usuarios/', UsuariosViewSet.as_view({'get': 'list', 'post': 'create'}), name='usuarios'),
    path('usuarios/<int:pk>/', UsuariosViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    # Categorias OK
    path('categorias/', CategoriaList.as_view(), name='categorias'),
    path('categorias/<int:pk>/', CategoriaDetail.as_view(), name='categoria_detail1'),

    # Carro OK
    path('carrito/', CarritoList.as_view(), name='carrito-list'),
    path('carrito/<int:pk>/', CarritoDetail.as_view(), name='carrito-detail'),
    path('pedircarrito/<int:pk>/', DeCarritoAPedido.as_view(), name='carrito-pedido'),

    # Pedido OK
    path('pedidos/', PedidoList.as_view(), name='pedidos-list'),
    path('pedidos/<int:pk>/', PedidoDetail.as_view(), name='pedidos-detail'),
    path('estadisticapedidos/<int:pk>/', EstadisticaPedidos.as_view(), name='pedidos-estadistica'),

    # Ok
    path('articulospedido/', ArticuloPedidoList.as_view(), name='articulospedido'),
    path('articulospedido/<int:pk>/', ArticuloPedidoDetail.as_view()),
    path('estadisticasarticuloscategorias/', estadisticasPedidos.as_view()),

    # Graficos
    path('cantidadusuarios/', usuariosPorTipo.as_view()),

    path('pago/', PagoList.as_view(), name='pago'),
    path('pago/<int:pk>/', PagoDetail.as_view()),
    path('estadisticapagos/<int:pk>/', EstadisticaPagos.as_view()),

    path('publicacion/', PublicacionList.as_view(), name='publicacion'),
    path('publicacion/<int:pk>/', PublicacionDetail.as_view()),

    path('puntuacionvendedor/', PuntuacionVendedorList.as_view(), name='puntuacionvendedor'),
    path('puntuacionvendedor/<int:pk>/', PuntuacionVendedorDetail.as_view()),

    # path('contact/', ContactView,name='contact'),
    # path('contact/', ContactEmail.as_view(),name='contact'),
    path('apis/', apis,name='apis'),
]

handler404 = 'Buy.views.handler404'