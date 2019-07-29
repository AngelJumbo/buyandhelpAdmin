from django.db import models

# Create your models here.

class Rol(models.Model):
    id_rol=models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)

class Usuario(models.Model):
    id_usuario= models.IntegerField(primary_key=True)
    id_rol= models.ForeignKey(Rol,on_delete=models.CASCADE)
    cedula= models.CharField(max_length=10)
    contrasenia= models.CharField(max_length=20)
    nombres= models.CharField(max_length=20)
    apellidos= models.CharField(max_length=20)
    email= models.CharField(max_length=20)
    direccion=models.CharField(max_length=40)

class Categoria(models.Model):
    id_categoria:models.IntegerField(primary_key=True)
    nombre: models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50)

class Articulo(models.Model):
    id_articulo= models.IntegerField(primary_key=True)
    id_categoria= models.ForeignKey(Categoria,on_delete=models.CASCADE)
    id_usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    nombre= models.CharField(max_length=10)
    precio=models.FloatField
    descripcion = models.CharField(max_length=10)
    donacion=models.FloatField

class EstadoPedido(models.Model):
    id_estado_pedido= models.IntegerField(primary_key=True)
    tipo=models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)

class Pedido(models.Model):
    id_pedido=models.IntegerField(primary_key=True)
    id_estado_pedido= models.ForeignKey(EstadoPedido,on_delete=models.CASCADE)
    fecha=models.DateField
    total_venta=models.FloatField
    id_comprador=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    id_vendedor= models.ForeignKey(Usuario,on_delete=models.CASCADE)
    entrega_a_tiempo=models.BooleanField

class ArticuloPedido(models.Model):
    id_articulo_pedido= models.IntegerField(primary_key=True)
    id_articulo=models.ForeignKey(Articulo,on_delete=models.CASCADE)
    id_pedido=models.ForeignKey(Pedido,on_delete=models.CASCADE)
    cantidad=models.IntegerField

class TipoPago(models.Model):
    id_tipo_pago = models.IntegerField(primary_key=True)
    tipo= models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)

class Pago(models.Model):
    id_pago=models.IntegerField(primary_key=True)
    id_tipo_pago = models.ForeignKey(TipoPago,on_delete=models.CASCADE)
    id_pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    fecha_pago= models.DateField

class Publicacion(models.Model):
    id_publicacion=models.IntegerField(primary_key=True)
    id_vendedor=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    id_articulo=models.ForeignKey(Articulo,on_delete=models.CASCADE)
    fecha_publicacion=models.DateField

class PuntuacionVendedor(models.Model):
    id_asignacion=models.IntegerField(primary_key=True)
    id_vendedor=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    id_comprador=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    puntuacion=models.IntegerField

