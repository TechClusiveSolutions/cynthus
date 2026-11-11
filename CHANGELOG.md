# Changelog

All notable changes to cynthus-documentation are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the versions follow
[Semantic Versioning](https://semver.org/). The Cynthus ecosystem release that bundles
each version is listed in the `cynthus` documentation repository.

Every pull request adds a line under `Unreleased`; a release renames that section to the
version and date.

## [Unreleased]

- The draft 1.0 release manifest now pins cynthus-shared v0.11.1 (selectable signal broker) and records that the dev stack has run on RabbitMQ. Issue 36.
- Added ADR-007, the decision to make the signal broker selectable by environment (`SIGNAL_BROKER`: Azure Service Bus by default, or RabbitMQ). It records the RabbitMQ topology (topic exchange, quorum queue per subscription, dead-letter queues, delivery limit, publisher confirms), the behaviour both brokers must share, and what RabbitMQ lacks. ADR-006 is marked partly superseded and engineering standards section 6 now describes the selectable broker.
- Added the ecosystem release manifest: `releases/README.md` explains the versioning scheme (ecosystem manifest, per-app SemVer, a separate signal schema version) and `releases/1.0.md` is the draft 1.0 set pinning every repo's current tag.

## [0.1.0] - 2026-11-10

- Align documents with the messaging-library model; add cynthus-device (#13)
- Render behavioural namespace tests (#6)
- Catalog the Shopping signals and document the Shopping design (#27) (#29)
- Catalog the chat message requested and generated signals (#24)
- Catalog the inventory owner added and removed facts (#21)
- Add the profile signals to the signal catalog (#19)
- Add the identity audit signals to the signal catalog (#17)
- Add inventory shelf signals to the signal catalog (#15)
- Consolidate master design documents (#10)
- Reorganize design documents into master PRD, architecture and roadmap (#8)
- Establish the Cynthus engineering workflow (#1) (#2)
- Add architecture notes and the cross-repository test tooling
- Initial commit
