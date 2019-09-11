from django.urls import path
from .views import index1
from django.conf.urls import url
from .views import *
from django.conf.urls import handler404


urlpatterns = [
    path('', index1, name='index'),
    path('articulos/',ArticulosList.as_view(), name ='articulos'),
    path('articulos/<int:pk>/', ArticulosDetail.as_view()),

    path('usuarios/', UsuariosViewSet.as_view({'get': 'list', 'post': 'create'}), name='usuarios'),
    # path('usuarios/<int:pk>/', UsuarioDetail.as_view()),

    path('categorias/', CategoriaList.as_view(), name='categorias'),
    path('categorias/<int:pk>/', CategoriaDetail.as_view()),

    path('pedido/', PedidoList.as_view(), name='pedido'),
    path('pedido/<int:pk>/', PedidoDetail.as_view()),

    path('articulospedido/', ArticuloPedidoList.as_view(), name='articulospedido'),
    path('articulospedido/<int:pk>/', ArticuloPedidoDetail.as_view()),

    path('pago/', PagoList.as_view(), name='pago'),
    path('pago/<int:pk>/', PagoDetail.as_view()),

    path('publicacion/', PublicacionList.as_view(), name='publicacion'),
    path('publicacion/<int:pk>/', PublicacionDetail.as_view()),

    path('puntuacionvendedor/', PuntuacionVendedorList.as_view(), name='puntuacionvendedor'),
    path('puntuacionvendedor/<int:pk>/', PuntuacionVendedorDetail.as_view()),

    path('contact', ContactView.as_view(),name='contact'),
    path('apis', apis,name='apis'),
]

handler404 = 'Buy.views.handler404'