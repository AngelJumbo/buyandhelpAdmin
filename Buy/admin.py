from django.contrib import admin
from Buy.models import Usuario,Categoria,Articulo,Pedido,ArticuloPedido,\
    Pago,Publicacion,PuntuacionVendedor,Imagen

# Register your models here.

# admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Articulo)
admin.site.register(Pedido)
admin.site.register(ArticuloPedido)
admin.site.register(Pago)
admin.site.register(Publicacion)
admin.site.register(PuntuacionVendedor)
admin.site.register(Imagen)

