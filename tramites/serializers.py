from typing import ClassVar

from rest_framework import serializers

from .models import Comentario, Tramite


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields: ClassVar[list[str]] = ["id", "tramite","texto", "fecha_creacion"]


class TramiteSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = Tramite
        fields: ClassVar[list[str]] = [
            "id",
            "nombre",
            "descripcion",
            "estado",
            "responsable",
            "correo_responsable",
            "fecha_creacion",
            "fecha_actualizacion",
            "comentarios",
        ]