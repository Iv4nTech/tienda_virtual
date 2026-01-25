from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from datetime import date
from django.forms import ValidationError


class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre', 'modelo', 'unidades', 'precio', 'vip', 'marca']

class CompraForm(ModelForm):

    promocion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Introduce código de descuento'})
    )
    class Meta:
        model = Compra
        fields = ['unidades', 'promocion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.promocion:
            self.fields['promocion'].initial = self.instance.promocion.codigo

    def clean_promocion(self):
        codigo = self.cleaned_data.get('promocion')
        if not codigo:
            return None

        try:
            promocion = Promocion.objects.get(codigo=codigo)
            if promocion.fecha_fin < date.today():
                raise forms.ValidationError('Este codigo caduco')
            return promocion
        except Promocion.DoesNotExist:
            raise forms.ValidationError("Este código no existe.")


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
        
    def clean(self):
        if self.cleaned_data['fecha_fin'] < date.today():
            raise ValidationError('La fecha de fin no puede ser anterior a la fecha actual')

