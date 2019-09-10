from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

''' 
class Rol(models.Model):
    id_rol=models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s: %s' % (self.id_rol, self.tipo)
'''

VENDEDOR = 'VEN'
COMPRADOR = 'COM'
roles = (
    (VENDEDOR, 'Vendedor'),
    (COMPRADOR, 'Comprador')
)

class Usuario(AbstractUser):

    regex_cedula = r'[0-9]{10}'
    rol = models.CharField(choices=roles, max_length=5, null=False, blank=False, default='COM')
    cedula= models.CharField(max_length=10, validators=[RegexValidator(regex_cedula)], null=False, blank=False)
    direccion=models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Categoria(models.Model):
    nombre= models.CharField(max_length=30, null=False, blank=False)
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Articulo(models.Model):
    categoria= models.ForeignKey(Categoria,on_delete=models.CASCADE, null=False, blank=False)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE, null=False, blank=False)
    nombre= models.CharField(max_length=30, null=False, blank=False)
    precio=models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    donacion=models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    descrip = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.nombre, self.usuario.__str__(), self.categoria.__str__())


class Imagen(models.Model):
    imagen=models.ImageField(upload_to='imagenes/',blank=False, null=False)
    articulo=models.ForeignKey(Articulo,on_delete=models.CASCADE,related_name="imagenes", null=False, blank=False)

    def __str__(self):        
        return self.articulo.__str__()


EMPACANDO = 'EMP'
EN_CAMINO = 'ENC'
ENTREGADO = 'ENT'

estados = (
    (EMPACANDO, 'Empacando'),
    (EN_CAMINO, 'En Camino'),
    (ENTREGADO, 'Entregado'),
)

class Pedido(models.Model):
    estado_pedido = models.CharField(max_length=10, null=False, blank=False, choices=estados, default='EMP')
    fecha=models.DateField(default=timezone.now().date(), null=False, blank=False)
    total_venta=models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], null=False, blank=False)
    comprador=models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name = 'comprador_pedido', null=False, blank=False)
    vendedor= models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name = 'vendedor_pedido', null=False, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.estado_pedido, self.comprador)


class ArticuloPedido(models.Model):
    articulo=models.ForeignKey(Articulo,on_delete=models.CASCADE, null=False, blank=False)
    pedido=models.ForeignKey(Pedido,on_delete=models.CASCADE, null=False, blank=False)
    cantidad=models.IntegerField(default=None, null=False, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.articulo.__str__(), self.pedido.__str__())


EFECTIVO = 'EFC'
TARJETA = 'TAR'

tipo_pagos = (
    (EFECTIVO, 'Efectivo'),
    (TARJETA, 'Tarjeta')
)

class Pago(models.Model):
    tipo_pago = models.CharField(max_length=10, null=False, blank=False, choices=tipo_pagos, default=EFECTIVO)
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    fecha_pago= models.DateField(default=None)

    def __str__(self):
        return '{} - {}'.format(self.tipo_pago, self.pedido.__str__())


class Publicacion(models.Model):
    vendedor=models.ForeignKey(Usuario,on_delete=models.CASCADE, null=False, blank=False)
    articulo=models.ForeignKey(Articulo,on_delete=models.CASCADE, null=False, blank=False)
    fecha_publicacion=models.DateField(default=timezone.now().date(), null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.vendedor.__str__(), self.articulo.__str__())


class PuntuacionVendedor(models.Model):
    vendedor=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name = 'vendedor_puntuacion', blank=True, null=True)
    comprador=models.ForeignKey(Usuario, default=1, on_delete=models.SET_DEFAULT,related_name = 'comprador_puntuacion', blank=True, null=True)
    puntuacion=models.IntegerField(default=0, validators=[MaxValueValidator(10)], null=False, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.vendedor.__str__(), self.puntuacion)

  
