# Infrastructure: versions and first-time setup

What the Cynthus stacks run on, and the order to start them for the first time. The repository READMEs leave the
versions out on purpose; this is where they are recorded. Versions come from the Dockerfiles and compose files, and
from the running stack on JMac on 2026-11-13.

---

## Versions

- PostgreSQL
  - Image: `postgres:${DB_VERSION}`, built by each segment's `containers/db/Dockerfile` from the `DB_DRIVER` and
    `DB_VERSION` settings in `.env`.
  - Running on JMac: 18.0 (`DB_DRIVER=postgres`, `DB_VERSION=18.0` in core, trust and intelligence).
- Redis
  - Image: `redis:alpine`, in each segment's `containers/cache/Dockerfile`. It is not pinned, so a rebuild can move
    to a newer Redis.
  - Running on JMac: the core cache reports Redis 8.10.3.
- RabbitMQ
  - Image: `rabbitmq:4.4-management` (`cynthus-emulators`, off unless the `rabbitmq` profile is used).
  - Running on JMac: 4.4.0.
- Mail sink
  - Image: Mailpit `v1.21.8` (`cynthus-emulators`, `containers/mail`).
- Azure Service Bus emulator
  - Image: `mcr.microsoft.com/azure-messaging/servicebus-emulator:latest`, with its store on
    `mcr.microsoft.com/azure-sql-edge` (`cynthus-emulators`). Neither is pinned.
- Python
  - Service containers run the Python 3 of `cynthus-base` (Debian bookworm); the services are tested on Python 3.11.
  - `cynthus-base` is `debian:bookworm-slim` with a virtual environment in `/opt/python`.

To change a version, change it in one place and rebuild: `DB_VERSION` in `.env` for PostgreSQL, the `FROM` line for
Redis, the `image:` line for RabbitMQ. A PostgreSQL major version does not upgrade in place: a data volume made by
one major version needs a dump and restore to move to another.

## What each segment has

Each segment has its own database and cache container, on its own internal network, and joins the shared
`cynthus_net` network for everything else.

- `cynthus-trust` (Auth): `cynthus-auth-db`, `cynthus-auth-cache`.
- `cynthus-core`: `cynthus-core-db`, `cynthus-core-cache`.
- `cynthus-intelligence`: `cynthus-intel-db`, `cynthus-intel-cache`.
- `cynthus-health`: `cynthus-portal-db`, `cynthus-portal-cache`.

The shared services, from `cynthus-emulators`: the mail sink (`cynthus-infra-mail`), the RabbitMQ broker
(`cynthus-infra-rabbitmq`) and the Service Bus emulator (`cynthus-infra-messaging` with `cynthus-infra-store`).
The segments do not share a PostgreSQL or a Redis, on purpose: each can run alone when another is down or under
attack (ADR-014, which supersedes ADR-012).

## First-time setup

Do this once on a new host, with Docker and the Compose plugin installed and network access to GitHub.

1. Create the shared network: `docker network create cynthus_net`.
2. Clone the repositories you need (`cynthus-emulators`, `cynthus-trust`, `cynthus-core`, and the others).
3. In each repository, create `.env` next to `docker-compose.yml` from the "Minimal configuration" list in its
   README. `.env` is git-ignored and holds secrets: never commit it.
   - Use the same `SIGNAL_BROKER` in every stack, with the matching `RABBITMQ_URL` or Service Bus settings.
   - Generate the Auth signing key once: `openssl genrsa 2048 | base64 -w0`, as `AUTH_JWT_PRIVATE_KEY_B64`.
4. Start the shared services first, from `cynthus-emulators`:
   - `docker compose up -d` for the mail sink and the Service Bus emulator;
   - `docker compose --profile rabbitmq up -d rabbitmq` for RabbitMQ, with `RABBITMQ_PASSWORD` already set.
5. Start Auth next, from `cynthus-trust`: `docker compose up -d --build`. The core services fetch their token keys
   from it, and Auth applies its database migrations when it starts.
6. Start the other segments: `docker compose up -d --build` in `cynthus-core`, then `cynthus-intelligence` (and
   `cynthus-health`).
7. Check each stack with `docker compose ps`: every container should be `healthy`.

## Gotchas

- PostgreSQL runs a container's initialisation scripts only when its data volume is empty. To re-run them, remove
  the volume (this deletes the data).
- Set the RabbitMQ password before the first start: the broker stores its user in its data volume.
- The Service Bus emulator has a small connection limit (10 by default) that a full stack exceeds; use RabbitMQ for a
  whole-stack run.
- Docker on a Mac runs under Colima, which shares only the home directory with its virtual machine: bind mounts from
  `/tmp` appear empty.
