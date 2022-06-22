from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome','email','senha')
    search_fiels = ('nome', 'email')
    readonly_fields = ('senha',)