from django.urls import path
from .views import *

urlpatterns = [
    path('tienda/admin/productos', ver_productos.as_view(), name='ver_producto'),
    path('tienda/admin/productos/<int:pk>', detalle_producto.as_view(), name='detalle_producto')
]
