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
    path('tienda/informes', informes, name='informes'),

    path('tienda/register', RegistroView.as_view(), name='register'),
    
    path('tienda/informe/compra/detalle/<int:pk>', detailCompra.as_view(), name='detalle_compra' ),

    path('tienda/admin/promociones', ViewPromociones.as_view(), name='ver_promociones'),
    path('tienda/admin/promociones/crear', CreatePromocion.as_view(), name='crear_promocion'),
    path('tienda/admin/promociones/<int:pk>', DetailPromocion.as_view(), name='detalle_promocion'),
    path('tienda/admin/promociones/editar/<int:pk>', UpdatePromocion.as_view(), name='editar_promocion'),
    path('tienda/admin/promociones/eliminar/<int:pk>', DeletePromocion.as_view(), name='eliminar_promocion')
]
