from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Comentario, Tramite
from .serializers import ComentarioSerializer, TramiteSerializer
from .tasks import notificar_creacion_tramite


class TramiteViewSet(viewsets.ModelViewSet):
    queryset = Tramite.objects.prefetch_related("comentarios").all()
    serializer_class = TramiteSerializer

    def create(self, request: Request, *args: object, **kwargs: object) -> Response:
        response = super().create(request, *args, **kwargs)
        notificar_creacion_tramite.delay(response.data["id"], response.data["nombre"])
        return response

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer