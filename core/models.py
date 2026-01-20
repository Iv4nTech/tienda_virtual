from django.db import models
from django.contrib.auth.models import AbstractUser

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

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
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.id} | {self.nombre} ({self.modelo}) Stock: {self.unidades}'
    
class Compra(models.Model):
    fecha = models.DateField(auto_now_add=True)
    unidades = models.IntegerField()
    importe = models.DecimalField(decimal_places=2, max_digits=6)
    iva = models.IntegerField()
    usuario = models.ForeignKey(UsuarioTienda, on_delete=models.SET_NULL, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.id} | {self.usuario} - {self.producto} UD: {self.unidades} [{self.fecha}]'