from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import *
from .forms import ProductoForm
from django.urls import reverse_lazy

class ver_productos(ListView):
    template_name = 'core/ver_productos.html'
    context_object_name = 'productos'
    model = Producto
    
class detalle_producto(DetailView):
    model = Producto
    context_object_name = 'producto'
    template_name = 'core/detalle_producto.html'

class crear_producto(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('ver_producto')
    template_name = 'core/crear_producto.html'

class editar_producto(UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('ver_producto')
    template_name = 'core/crear_producto.html'

class eliminar_producto(DeleteView):
    model = Producto
    success_url = reverse_lazy('ver_producto')
    template_name = 'core/eliminar_producto.html'
    context_object_name = 'producto'