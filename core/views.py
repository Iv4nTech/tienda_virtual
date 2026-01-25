from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import *
from .forms import ProductoForm, CompraForm, ClienteCreationForm, PromocionesForm
from django.urls import reverse_lazy
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from django.db.models import Count, Avg

def user_admin_or_staff(user):
    return user.is_superuser or user.is_staff


class ver_productos(UserPassesTestMixin,ListView):
    template_name = 'core/ver_productos.html'
    context_object_name = 'productos'
    model = Producto

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
class detalle_producto(UserPassesTestMixin,DetailView):
    model = Producto
    context_object_name = 'producto'
    template_name = 'core/detalle_producto.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class crear_producto(UserPassesTestMixin,CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('ver_producto')
    template_name = 'core/crear_producto.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class editar_producto(UserPassesTestMixin,UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('ver_producto')
    template_name = 'core/crear_producto.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class eliminar_producto(UserPassesTestMixin,DeleteView):
    model = Producto
    success_url = reverse_lazy('ver_producto')
    template_name = 'core/eliminar_producto.html'
    context_object_name = 'producto'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class ver_productos_tienda(ListView):
    model = Producto
    context_object_name = 'productos'
    template_name = 'core/ver_productos_tienda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Marca.objects.all()
        try:
            context['price'] = int(self.request.GET.get('price'))
        except TypeError:
             context['price'] = self.request.GET.get('price')
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
           queryset = queryset.filter(precio__lt = self.request.GET.get('price'))
       return queryset
    
@login_required
def checkout(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form =  CompraForm(request.POST)
        if form.is_valid():
            nueva_compra = form.save(commit=False)
            nueva_compra.producto = producto
            nueva_compra.importe = (float(producto.precio * form.cleaned_data['unidades']) * 1.21) * (form.cleaned_data['promocion'].descuento/100)
            nueva_compra.usuario = request.user
            nueva_compra.save()
            return redirect('ver_producto_tienda')
    else:
        form = CompraForm()
    return render(request, 'core/checkout.html', {'form':form, 'producto':producto})

class CheckoutCreateView(LoginRequiredMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'core/checkout.html'
    success_url = reverse_lazy('ver_producto_tienda')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['producto'] = get_object_or_404(Producto, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        producto = get_object_or_404(Producto, pk=self.kwargs['pk'])
        form.instance.usuario = self.request.user
        form.instance.producto = producto
        unidades = form.cleaned_data['unidades']
        descuento = form.cleaned_data['promocion'].descuento
        
        form.instance.importe = (float(producto.precio * unidades) * 1.21) * (descuento / 100)
        
        return super().form_valid(form)

@user_passes_test(user_admin_or_staff)
def informes(request):
    marca_request = request.GET.get('marcas')
    productos = Producto.objects.annotate(Sum('compras__unidades')).order_by('-compras__unidades__sum')
    marca_filtrada = Marca.objects.filter(nombre=marca_request).first()
    marcas = Marca.objects.all()
    clientes_importe = UsuarioTienda.objects.annotate(importe_total_compras=Sum('compras__importe'))

    username = request.GET.get('username')
    user = UsuarioTienda.objects.filter(username=username).first()
    compra = Compra.objects.filter(usuario=user)
  
    mejores_diez_importes = UsuarioTienda.objects.annotate(Sum('compras__importe')).order_by('-compras__importe__sum')
    

    return render(request, 'core/informes.html', {'productos':productos, 'marcas':marcas, 'marcafiltrada':marca_filtrada, 'compras':compra, 'topdiez':mejores_diez_importes})

class RegistroView(CreateView):
    form_class = ClienteCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class detailCompra(DetailView):
    model = Compra
    template_name = 'core/detalle_compra.html'
    context_object_name = 'compra'

class ViewPromociones(ListView):
    model = Promocion
    context_object_name = 'promociones'
    template_name = 'core/ver_promociones.html'

class CreatePromocion(CreateView):
    model = Promocion
    form_class = PromocionesForm
    success_url = reverse_lazy('ver_promociones')
    template_name = 'core/crear_promocion.html'

class DetailPromocion(DetailView):
    model = Promocion
    template_name = 'core/detalle_promocion.html'

class DeletePromocion(DeleteView):
    model = Promocion
    template_name = 'core/eliminar_promocion.html'
    success_url = reverse_lazy('ver_promociones')

class UpdatePromocion(UpdateView):
    model = Promocion
    template_name = 'core/crear_promocion.html'
    success_url = reverse_lazy('ver_promociones')
    form_class = PromocionesForm

def ver_informe_promociones(request):
    query = Promocion.objects.annotate(Count('compras'))
    total_promos = Promocion.objects.aggregate(Count('compras'))
    media_compras_promo = Promocion.objects.aggregate(Avg('compras__promocion__descuento'))
    return render(request, 'core/informe_promociones.html', {'promociones':query, 'total':total_promos, 'descuento_medio':media_compras_promo})
