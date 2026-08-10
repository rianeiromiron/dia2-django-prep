import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Tramite

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Tramite)
def log_tramite_creado(sender: type[Tramite], instance: Tramite, created: bool, **kwargs: object) -> None:
    if created:
        logger.info("Signal: nuevo Tramite creado - id=%s, nombre=%s", instance.id, instance.nombre)