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

class ver_productos_tienda(ListView):
    model = Producto
    context_object_name = 'productos'
    template_name = 'core/ver_productos_tienda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Marca.objects.all()
        return context
    
    def get_queryset(self):
       queryset = super().get_queryset()
       if self.request.GET.get('name-product'):
           queryset = queryset.filter(nombre__icontains=self.request.GET.get('name-product'))
       elif self.request.GET.get('brand'):
           marca = self.request.GET.get('brand')
           id_marca = Marca.objects.filter(nombre=marca).values()[0]['id']
           print(id_marca)
           queryset = queryset.filter(marca=id_marca)
       elif self.request.GET.get('vip'):
           queryset = queryset.filter(vip=True)
       elif self.request.GET.get('price'):
           queryset = queryset.filter(precio=self.request.GET.get('price'))
       return queryset


           