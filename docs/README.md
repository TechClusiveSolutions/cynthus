# Cynthus documentation index

| Document | What it is | Version |
|---|---|---|
| [PRD.md](PRD.md) | Master product requirements | 4.2 (June 2026) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Master architectural design document | 6.0 (June 2026) |
| [ROADMAP.md](ROADMAP.md) | Master roadmap (draft) | 0.1 |
| [features/feature-registry.md](features/feature-registry.md) | Feature map: tiers, features, phases, booster packs | 1.1 |
| [signals/signal-catalog.md](signals/signal-catalog.md) | Signal map: every signal by domain | 1.0 |
| [signals/signal-list-by-service.md](signals/signal-list-by-service.md) | Signals published/consumed per service (draft, mostly empty) | draft |
| [signals/signal-handling-matrix.md](signals/signal-handling-matrix.md) | Older per-service publisher/consumer matrix; to be folded into the list above | 2026-06-01 |
| [adr/](adr) | Architecture decision records | |
| [architecture/](architecture) | System topology blueprint (to fold into ARCHITECTURE.md) and the web-app conversion plan | |
| [engineering-standards.md](engineering-standards.md) | How we write, test, review and merge code | |
| [archive/](archive) | Superseded drafts, kept for history. `archive/vesta` is the predecessor project (Selda/Vesta). | |

Conventions: masters carry no date or version in the file name; the version and a changelog live inside the file.
Superseded files move to `archive/`; nothing is deleted.

## Known inconsistencies to resolve
- The signal catalog cites Feature Registry v1.4; the registry is v1.1.
- The feature registry cites PRD v4.1; the PRD is 4.2.
- The signal-by-service list and handling matrix overlap; merge them.
