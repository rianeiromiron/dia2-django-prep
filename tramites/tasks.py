import logging
import time

from celery import shared_task

from .models import EventoOutbox

logger = logging.getLogger(__name__)


@shared_task
def notificar_creacion_tramite(tramite_id: int, nombre: str) -> str:
    logger.info("Procesando notificación para trámite %s (%s)...", tramite_id, nombre)
    time.sleep(3)  # Simula una llamada lenta a un servicio externo (email, SMS, etc.)
    mensaje = f"Notificación enviada: el trámite '{nombre}' (id={tramite_id}) fue creado"
    logger.info(mensaje)
    return mensaje

@shared_task
def publicar_eventos_pendientes() -> str:
    eventos = EventoOutbox.objects.filter(publicado=False)
    contador = 0

    for evento in eventos:
        if evento.tipo == "tramite.creado":
            notificar_creacion_tramite.delay(
                evento.payload["id"],
                evento.payload["nombre"],
            )
        evento.publicado = True
        evento.save()
        contador += 1

    return f"{contador} eventos publicados"