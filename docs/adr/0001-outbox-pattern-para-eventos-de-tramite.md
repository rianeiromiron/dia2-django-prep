# 0001 - Usar el Outbox Pattern para publicar eventos de Trámite

## Status
Aceptado

## Context
Al crear un `Tramite`, el sistema necesita notificar a otros procesos (inicialmente,
una tarea de Celery que envía una notificación). La primera implementación llamaba
directamente a `.delay()` dentro de `TramiteViewSet.create()`, justo después de
guardar el registro en la base de datos.

Este enfoque tiene un problema conocido como "dual write": si el guardado en base
de datos tiene éxito pero la llamada a Redis (broker de Celery) falla por cualquier
razón (timeout, Redis caído momentáneamente), el `Tramite` queda creado pero el
evento nunca se publica, sin ningún error visible para el usuario ni el equipo.

## Decision
Implementar el patrón Outbox: cada evento de negocio se escribe en una tabla
`EventoOutbox`, en la misma transacción de base de datos (`transaction.atomic()`)
que el cambio de negocio que lo origina. Un proceso separado (`publicar_eventos_pendientes`,
pensado para correr periódicamente vía Celery Beat) es la única fuente de verdad
que lee eventos pendientes y dispara las tareas de Celery correspondientes.

Se eliminó la llamada directa a `.delay()` dentro del ViewSet para evitar
duplicación de eventos (ver Consequences).

## Consequences

**Positivas:**
- Garantiza que un evento de negocio nunca se pierde, incluso si el broker
  de mensajería está temporalmente no disponible.
- Consistencia transaccional real entre el dato de negocio y el evento.

**Negativas:**
- Introduce latencia entre la creación del recurso y la publicación real del
  evento (depende de la frecuencia con la que corra el publicador).
- Requiere infraestructura adicional (una tabla más, un proceso periódico) en
  comparación con la llamada directa.

**Riesgo detectado durante la implementación:** durante el desarrollo, se mantuvo
temporalmente la llamada directa a `.delay()` coexistiendo con el publicador del
Outbox, causando que la misma notificación se disparara dos veces para el mismo
evento (verificado con logs del worker). Corregido eliminando la llamada directa,
dejando el Outbox como única fuente de verdad de publicación.