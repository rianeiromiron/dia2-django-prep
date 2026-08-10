from django.db import transaction
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Comentario, EventoOutbox, Tramite
from .serializers import ComentarioSerializer, TramiteSerializer


class TramiteViewSet(viewsets.ModelViewSet):
    queryset = Tramite.objects.prefetch_related("comentarios").all()
    serializer_class = TramiteSerializer

    def create(self, request: Request, *args: object, **kwargs: object) -> Response:
        with transaction.atomic():
            response = super().create(request, *args, **kwargs)
            EventoOutbox.objects.create(
                tipo="tramite.creado",
                payload={"id": response.data["id"], "nombre": response.data["nombre"]},
            )
        return response


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer