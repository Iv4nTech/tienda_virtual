from django.urls import path
from .views import *

urlpatterns = [
    path('tienda/admin/productos', ver_productos.as_view(), name='ver_producto'),
    path('tienda/admin/productos/<int:pk>', detalle_producto.as_view(), name='detalle_producto'),
    path('tienda/admin/productos/nuevo', crear_producto.as_view(), name='crear_producto'),
    path('tienda/admin/productos/edicion/<int:pk>', editar_producto.as_view(), name='editar_producto'),
    path('tienda/admin/productos/eliminar/<int:pk>', eliminar_producto.as_view(), name='eliminar_producto'),

    path('tienda/compra/', ver_productos_tienda.as_view(), name='ver_producto_tienda'),
    path('tienda/checkout/<int:pk>', checkout, name='checkout'),
    path('tienda/informes', informes, name='informes')
]
