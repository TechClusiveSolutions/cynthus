# ADR-006: FastStream adapter for Azure Service Bus

**Status:** Accepted (2026-11-01)
**Supersedes:** the assumption in earlier notes that `faststream[azure]` and `faststream.azure` exist.

## Context

The architecture (ADD v6, section 5) uses Azure Service Bus with three topics as the messaging backbone, and the
services are FastAPI applications that use FastStream. The code written so far imports `faststream.azure`
(`AzureServiceBusRouter`, `AzureServiceBusSubscription`, `AzureServiceBusTopic`). **That module does not exist** in any
FastStream release (checked against 0.7.2 and the latest 0.7.8): FastStream ships Kafka, Confluent, RabbitMQ, NATS and
Redis brokers only. The FastStream maintainers closed the Azure request (ag2ai/faststream#822, 2026-05-25) with
"Azure Service Bus support isn't on our roadmap"; from 1.0 only the common brokers stay in the core and others are
"community-driven".

## Options considered

| Option | Verdict |
|---|---|
| `faststream-azure-servicebus` (PyPI, MIT, by Thomas Laich) | **Chosen.** The only FastStream broker for Azure Service Bus. Listed under *Community Extensions* in the FastStream documentation (ag2ai/faststream#3308, merged 2026-10-28). Topics and subscriptions, request/reply, peek-lock settlement, batching, scheduled messages, OpenTelemetry/Prometheus extras, AsyncAPI, a `TestServiceBusBroker` for offline tests, and FastAPI integration through `faststream-fastapi`. Depends on `faststream>=0.7,<0.8` and `azure-servicebus>=7.14,<8`; Python >= 3.10. |
| Use `azure-servicebus` directly and write our own consumer loops | The fallback. Already used in `routes/signal.py`. Loses FastStream's routing, dependency injection, AsyncAPI and test broker; every service re-implements settlement and error handling. |
| Wrap Azure Service Bus's AMQP endpoint with FastStream's generic AMQP support | FastStream has no generic AMQP broker. Rejected. |
| Switch the backbone to RabbitMQ/NATS/Kafka | Contradicts ADD v6 and the Azure deployment. Rejected. |
| Write and maintain our own FastStream broker | Large, unrelated engineering cost. Rejected for now. |

## Decision

Use **`faststream-azure-servicebus`**, pinned to `>=0.2.1,<0.3`, with `faststream-fastapi` for the FastAPI integration.
Do not let application code depend on it directly:

- Services publish through the `SignalPublisher` interface and subscribe through the `SignalSubscriber` interface
  (one class per module). The adapter is wired in exactly one place, the application lifespan.
- Unit tests use the adapter's `TestServiceBusBroker`, or an in-memory fake of the interfaces.

## Consequences

- **Risk: young, single-maintainer project.** Four releases between 2026-08-24 and 2026-10-06, 22 commits, one
  contributor, no stars. Mitigations: the exact-version pin; the interface above, so the fallback (the plain Azure SDK)
  can replace it without touching application code; a review trigger below.
- **Known gaps** (stated in its README): sessions, deferred-message retrieval and dead-letter-queue consumption are not
  implemented. None is needed for the choreographed signals in phase 1. Dead-lettering is available through
  peek-lock settlement.
- **Emulator limits** (Azure's emulator, not the adapter): entities are fixed at start-up, at most 50 per namespace and
  10 concurrent connections. The topic and subscription layout therefore lives in the emulator configuration file.
- The `faststream` version is capped below 0.8 until the adapter publishes support for it.
- Existing code importing `faststream.azure` (`cynthus-messaging-core` subscriptions, `cynthus-intelligence/analysis`)
  moves to the adapter's modules.

## Review triggers

Revisit this decision if any of these happens: the adapter has no release for six months; FastStream 0.8 or 1.0 ships
without adapter support; a security advisory is raised against it; or the maintainers publish an official Azure broker.

## Sources

- PyPI metadata for `faststream-azure-servicebus` 0.2.1 (requires faststream 0.7.x, azure-servicebus 7.x).
- <https://github.com/thomaslaich/faststream-azure-servicebus>
- <https://github.com/ag2ai/faststream/issues/822> and <https://github.com/ag2ai/faststream/pull/3308>
