from django.db import models


class Tramite(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        EN_REVISION = "EN_REVISION", "En revisión"
        APROBADO = "APROBADO", "Aprobado"
        RECHAZADO = "RECHAZADO", "Rechazado"

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    responsable = models.CharField(max_length=200, blank=True)
    correo_responsable = models.EmailField(blank=True)
    def __str__(self) -> str:
        return self.nombre

class Comentario(models.Model):
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE, related_name="comentarios")
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comentario en {self.tramite.nombre}"

class EventoOutbox(models.Model):
    tipo = models.CharField(max_length=100)
    payload = models.JSONField()
    publicado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.tipo} (publicado={self.publicado})"