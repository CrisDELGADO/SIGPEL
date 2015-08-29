from django.contrib import admin
from .models import *

# Register your models here.

'''
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('prov_codigo','prov_nombre')

admin.site.register(Provincia, ProvinciaAdmin)

class CiudadAdmin(admin.ModelAdmin):
    list_display = ('ciu_codigo','ciu_nombre','prov_codigo')

admin.site.register(Ciudad, CiudadAdmin)

class RolAdmin(admin.ModelAdmin):
    list_display = ('rol_codigo','rol_nombre','rol_clave')

admin.site.register(Rol,RolAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usu_codigo','usu_nombre','usu_apellido','usu_email','rol_codigo')
'''
admin.site.register(User)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Foto)
admin.site.register(Pedido)
admin.site.register(Publicidad)
admin.site.register(Rol)
admin.site.register(Provincia)
admin.site.register(Ciudad)

