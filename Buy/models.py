from django.db import models

# Create your models here.

class Rol(models.Model):
    id_rol=models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s: %s' % (self.id_rol, self.tipo)

class Usuario(models.Model):
    id_usuario= models.AutoField(primary_key=True)
    id_rol= models.ForeignKey(Rol,on_delete=models.CASCADE)
    cedula= models.CharField(max_length=10)
    contrasenia= models.CharField(max_length=20)
    nombres= models.CharField(max_length=20)
    apellidos= models.CharField(max_length=20)
    email= models.CharField(max_length=20)
    direccion=models.CharField(max_length=40)

    def __str__(self):
        return '%s: %s %s' % (self.id_usuario, self.nombres, self.apellidos)

class Categoria(models.Model):
    id_categoria=models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s: %s' % (self.id_categoria, self.nombre)

class Articulo(models.Model):
    id_articulo= models.AutoField(primary_key=True)
    id_categoria= models.ForeignKey(Categoria,on_delete=models.CASCADE)
    id_usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    nombre= models.CharField(max_length=30)
    precio=models.FloatField(default=None)
    donacion=models.FloatField(default=None)
    descrip = models.CharField(max_length=100)

    def __str__(self):
        return '%s: %s - %s' % (self.id_articulo, self.nombre, self.precio)

class EstadoPedido(models.Model):
    id_estado_pedido= models.AutoField(primary_key=True)
    tipo=models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s: %s' % (self.id_estado_pedido, self.tipo)

class Pedido(models.Model):
    id_pedido=models.AutoField(primary_key=True)
    id_estado_pedido= models.ForeignKey(EstadoPedido,on_delete=models.CASCADE)
    fecha=models.DateField(default=None)
    total_venta=models.FloatField(default=None)
    id_comprador=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name = 'comprador_pedido')
    id_vendedor= models.ForeignKey(Usuario, default=1, on_delete=models.SET_DEFAULT,related_name = 'vendedor_pedido')

    def __str__(self):
        return '%s: %s - %s' % (self.id_pedido, self.fecha, self.total_venta)

class ArticuloPedido(models.Model):
    id_articulo_pedido= models.AutoField(primary_key=True)
    id_articulo=models.ForeignKey(Articulo,on_delete=models.CASCADE)
    id_pedido=models.ForeignKey(Pedido,on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=None)

    def __str__(self):
        return '%s: Articulo: %s' % (self.id_articulo_pedido, self.id_articulo)


class TipoPago(models.Model):
    id_tipo_pago = models.AutoField(primary_key=True)
    tipo= models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s: %s' % (self.id_tipo_pago, self.tipo)

class Pago(models.Model):
    id_pago=models.AutoField(primary_key=True)
    id_tipo_pago = models.ForeignKey(TipoPago,on_delete=models.CASCADE)
    id_pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    fecha_pago= models.DateField(default=None)

    def __str__(self):
        return '%s: Fecha: %s' % (self.id_pago, self.fecha_pago)

class Publicacion(models.Model):
    id_publicacion=models.AutoField(primary_key=True)
    id_vendedor=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    id_articulo=models.ForeignKey(Articulo,on_delete=models.CASCADE)
    fecha_publicacion=models.DateField(default=None)

    def __str__(self):
        return '%s: Vendedor: %s Articulo: %s Fecha: %s' % (self.id_publicacion, self.id_vendedor,self.id_articulo, self.fecha_publicacion)

class PuntuacionVendedor(models.Model):
    id_asignacion=models.AutoField(primary_key=True)
    id_vendedor=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name = 'vendedor_puntuacion')
    id_comprador=models.ForeignKey(Usuario, default=1, on_delete=models.SET_DEFAULT,related_name = 'comprador_puntuacion')
    puntuacion=models.IntegerField(default=None)

    def __str__(self):
        return '%s: Vendedor: %s Puntuación: %s' % (self.id_asignacion, self.id_vendedor, self.puntuacion)

  
