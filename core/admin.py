from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class UserAdminTienda(UserAdmin):
    model = UsuarioTienda
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('vip', 'saldo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('vip', 'saldo')}),
    )

admin.site.register(UsuarioTienda, UserAdminTienda)
admin.site.register(Producto)
admin.site.register(Marca)
admin.site.register(Compra)
admin.site.register(Promocion)