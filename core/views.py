from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from .models import *

class ver_productos(ListView):
    template_name = 'core/ver_productos.html'
    context_object_name = 'productos'
    model = Producto
    
class detalle_producto(DetailView):
    model = Producto
    context_object_name = 'producto'
    template_name = 'core/detalle_producto.html'