from django.forms import ModelForm
from .models import *


class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre', 'modelo', 'unidades', 'precio', 'vip', 'marca']

