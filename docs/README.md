# Cynthus documentation index

- [PRD.md](PRD.md)
  - What it is: Master product requirements
  - Version: 4.2 (June 2026)
- [ARCHITECTURE.md](ARCHITECTURE.md)
  - What it is: Master architectural design document
  - Version: 6.0 (June 2026)
- [ROADMAP.md](ROADMAP.md)
  - What it is: Master roadmap: phases 1-8 from the PRD, plus engineering work before Phase 1
  - Version: 1.0
- [features/feature-registry.md](features/feature-registry.md)
  - What it is: Feature map: tiers, features, phases, booster packs
  - Version: 1.1
- [signals/signal-catalog.md](signals/signal-catalog.md)
  - What it is: Signal map: every signal by domain, with publishers and consumers
  - Version: 1.0
- [signals/signal-list-by-service.md](signals/signal-list-by-service.md)
  - What it is: The same signals viewed per service, plus discrepancies found
  - Version: 1.0
- [adr/](adr)
  - What it is: Architecture decision records
  - Version: none
- [architecture/](architecture)
  - What it is: Web-app conversion plan; [Shopping design](architecture/shopping-design.md)
  - Version: none
- [infrastructure.md](infrastructure.md)
  - What it is: Versions of PostgreSQL, Redis, RabbitMQ and the emulators, and first-time setup
  - Version: none
- [engineering-standards.md](engineering-standards.md)
  - What it is: How we write, test, review and merge code
  - Version: none
- [archive/](archive/README.md)
  - What it is: Superseded drafts, kept for history
  - Version: none

Conventions: masters carry no date or version in the file name; the version lives inside the file. Superseded files
move to `archive/`; nothing is deleted.

## Known gaps

These need a decision or a missing source from the document owner. None has been changed.

1. **The feature registry is behind the signal catalog.** The catalog cites Feature Registry v1.4; the registry in this
   repository is v1.1. The catalog uses 50 feature IDs that the registry does not define: FT-AI-002 to 005,
   FT-AM-008 to 010, FT-AX-003 to 006, FT-CL-003 to 005, FT-DA-004 to 008, FT-IM-011 to 013, FT-MP-011, FT-PL-001 to 004,
   FT-RM-006 to 011, FT-RP-005, FT-SI-001 to 003, FT-SL-001 to 011, FT-SR-006, 007. A newer registry may exist elsewhere.
2. **Companion citations disagree.** The registry cites PRD v4.1; the PRD is 4.2. ADD 6.0 cites PRD 4.2 and registry
   v1.1.
3. **Services the catalog uses that ADD 6.0 does not name:** `cynthus-shopping`, `cynthus-notification`,
   `spire-agent`, `spire-server`. Details are in
   [signals/signal-list-by-service.md](signals/signal-list-by-service.md).
4. **Group chat has no owner.** `cynthus-messaging` is the communication library, not a service, yet the catalog uses
   it as the group-chat publisher and consumer (12 rows), and ADD 6.0 lists a `cynthus-messaging-engine` hub.
5. **Chat transport conflicts.** ADD 6.0 has `cynthus-core-api` route user sessions to `cynthus-chat` over VNet peering and
   gRPC. The owner recalls the chat service talking to the user's device directly through an API, and says all
   communication goes over Service Bus topics. Not resolved.
6. **`cynthus-device` location.** Expected in `cynthus-health`; HUD and video data are not health-specific.
7. **Roadmap dates** are the PRD's. Phase 7 depends on regulatory approval.
