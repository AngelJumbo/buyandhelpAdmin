from django.contrib import admin
from Buy.models import Rol,Usuario,Categoria,Articulo,EstadoPedido,Pedido,ArticuloPedido,TipoPago,Pago,Publicacion,PuntuacionVendedor

# Register your models here.

admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Articulo)
admin.site.register(EstadoPedido)
admin.site.register(Pedido)
admin.site.register(ArticuloPedido)
admin.site.register(TipoPago)
admin.site.register(Pago)
admin.site.register(Publicacion)
admin.site.register(PuntuacionVendedor)

