import logging
import time
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class TiempoRespuestaMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        inicio = time.time()
        response = self.get_response(request)
        duracion = time.time() - inicio

        logger.info(
            "%s %s -> %s (%.3fs)",
            request.method,
            request.path,
            response.status_code,
            duracion,
        )
        return response