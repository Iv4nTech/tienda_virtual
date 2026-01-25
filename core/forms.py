from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre', 'modelo', 'unidades', 'precio', 'vip', 'marca']

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ['unidades']

class ClienteCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model() 
        fields = ('username', 'email', 'first_name', 'last_name')  

class PromocionesForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre', 'codigo', 'descuento', 'fecha_fin']

        widgets = {
            "fecha_fin": forms.DateInput(attrs={'type':'date'}),
            'descuento': forms.NumberInput(attrs={'type':'number','min':'0', 'max':'100', 'value':'0'})
        }
