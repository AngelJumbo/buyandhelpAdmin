from django.urls import path
from .views import index1
from django.conf.urls import url
from .views import *
from django.conf.urls import handler404


urlpatterns = [
    path('', index1, name='index'),
    url(r'^articulos/$',ArticulosList.as_view(), name ='articulos'),
    url(r'^articulos/(?P<pk>[0-9]+)/$', ArticulosDetail.as_view()),

    url(r'^roles/$',RolList.as_view(), name ='roles'),
    url(r'^roles/(?P<pk>[0-9]+)/$', RolDetail.as_view()),

    url(r'^usuarios/$', UsuarioList.as_view(), name='usuarios'),
    url(r'^usuarios/(?P<pk>[0-9]+)/$', UsuarioDetail.as_view()),

    url(r'^categorias/$', CategoriaList.as_view(), name='categorias'),
    url(r'^categorias/(?P<pk>[0-9]+)/$', CategoriaDetail.as_view()),

    url(r'^estadopedido/$', EstadoPedidoList.as_view(), name='estadopedido'),
    url(r'^estadopedido/(?P<pk>[0-9]+)/$', EstadoPedidoDetail.as_view()),

    url(r'^pedido/$', PedidoList.as_view(), name='pedido'),
    url(r'^pedido/(?P<pk>[0-9]+)/$', PedidoDetail.as_view()),

    url(r'^articulospedido/$', ArticuloPedidoList.as_view(), name='articulospedido'),
    url(r'^articulospedido/(?P<pk>[0-9]+)/$', ArticuloPedidoDetail.as_view()),

    url(r'^tipopago/$', TipoPagoList.as_view(), name='tipopago'),
    url(r'^tipopago/(?P<pk>[0-9]+)/$', TipoPagoDetail.as_view()),

    url(r'^pago/$', PagoList.as_view(), name='pago'),
    url(r'^pago/(?P<pk>[0-9]+)/$', PagoDetail.as_view()),

    url(r'^publicacion/$', PublicacionList.as_view(), name='publicacion'),
    url(r'^publicacion/(?P<pk>[0-9]+)/$', PublicacionDetail.as_view()),

    url(r'^puntuacionvendedor/$', PuntuacionVendedorList.as_view(), name='puntuacionvendedor'),
    url(r'^puntuacionvendedor/(?P<pk>[0-9]+)/$', PuntuacionVendedorDetail.as_view()),

    path('contact', ContactView.as_view(),name='contact'),
    path('apis', apis,name='apis'),
]

handler404 = 'Buy.views.handler404'