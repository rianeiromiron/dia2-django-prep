from django.contrib import admin

from .models import Comentario, Tramite


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1

@admin.register(Tramite)
class TramiteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "estado", "fecha_creacion", "fecha_actualizacion")
    list_filter = ("estado",)
    search_fields = ("nombre", "descripcion")
    inlines = [ComentarioInline]  # noqa: RUF012

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("tramite", "texto", "fecha_creacion")
    list_filter = ("tramite",)