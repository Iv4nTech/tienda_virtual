from django.db import models
from django.contrib.auth.models import AbstractUser

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.nombre}'

class UsuarioTienda(AbstractUser):
    vip = models.BooleanField(default=False)
    saldo = models.DecimalField(decimal_places=2, max_digits=4, null=True)

    def __str__(self):
        return f'{self.username}'
    
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=75)
    unidades = models.IntegerField()
    precio = models.DecimalField(decimal_places=2, max_digits=4)
    vip = models.BooleanField(default=False)
    usuario = models.ManyToManyField(UsuarioTienda, through='Compra')
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')

    def __str__(self):
        return f'{self.id} | {self.nombre} ({self.modelo}) Stock: {self.unidades}'
    
class Compra(models.Model):

    class Iva(models.IntegerChoices):
        GENERAL = 21
        REDUCIDO = 10
        SUPERREDUCIDO = 4
        EXCENTO = 0


    fecha = models.DateField(auto_now_add=True)
    unidades = models.IntegerField()
    importe = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    iva = models.IntegerField(choices=Iva, null=True)
    usuario = models.ForeignKey(UsuarioTienda, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras')

    def __str__(self):
        return f'{self.id} | {self.usuario} - {self.producto} UD: {self.unidades} [{self.fecha}]'
    
class Promocion(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=20)
    descuento = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
