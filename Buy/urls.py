from django.urls import path
from .views import index1
from django.conf.urls import url
from .views import *
from django.conf.urls import handler404


urlpatterns = [
    path('', index1, name='index'),
    url(r'^articulos/$',ArticulosList.as_view(), name ='articulos'),
    url(r'^articulos/<int:pk>/', ArticulosDetail.as_view()),

    url(r'^roles/$',RolList.as_view(), name ='roles'),
    url(r'^roles/<int:pk>/$', RolDetail.as_view()),

    url(r'^usuarios/$', UsuarioList.as_view(), name='usuarios'),
    url(r'^usuarios/<int:pk>/$', UsuarioDetail.as_view()),

    url(r'^categorias/$', CategoriaList.as_view(), name='categorias'),
    url(r'^categorias/<int:pk>/$', CategoriaDetail.as_view()),

    url(r'^estadopedido/$', EstadoPedidoList.as_view(), name='estadopedido'),
    url(r'^estadopedido/<int:pk>/$', EstadoPedidoDetail.as_view()),

    url(r'^pedido/$', PedidoList.as_view(), name='pedido'),
    url(r'^pedido/<int:pk>/$', PedidoDetail.as_view()),

    url(r'^articulospedido/$', ArticuloPedidoList.as_view(), name='articulospedido'),
    url(r'^articulospedido/<int:pk>/$', ArticuloPedidoDetail.as_view()),

    url(r'^tipopago/$', TipoPagoList.as_view(), name='tipopago'),
    url(r'^tipopago/<int:pk>/$', TipoPagoDetail.as_view()),

    url(r'^pago/$', PagoList.as_view(), name='pago'),
    url(r'^pago/<int:pk>/$', PagoDetail.as_view()),

    url(r'^publicacion/$', PublicacionList.as_view(), name='publicacion'),
    url(r'^publicacion/<int:pk>/$', PublicacionDetail.as_view()),

    url(r'^puntuacionvendedor/$', PuntuacionVendedorList.as_view(), name='puntuacionvendedor'),
    url(r'^puntuacionvendedor/<int:pk>/$', PuntuacionVendedorDetail.as_view()),

    path('contact', ContactView.as_view(),name='contact'),
    path('apis', apis,name='apis'),
]

handler404 = 'Buy.views.handler404'