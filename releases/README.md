# Cynthus ecosystem releases

An ecosystem release is a manifest, not a product. Each file in this folder lists the exact
version of every Cynthus app and library that was tested together, plus the signal schema
version they share.

## Version scheme

- Ecosystem
  - Scheme: `MAJOR.MINOR` manifest (this folder)
  - Where it lives: `releases/<version>.md`
- App or library
  - Scheme: Semantic Versioning, tag `vX.Y.Z` on the repo
  - Where it lives: git tag and the repo's `CHANGELOG.md`
- Signal schema
  - Scheme: Semantic Versioning, `SIGNAL_SCHEMA_VERSION` in cynthus-shared
  - Where it lives: cynthus-shared (issue 102)

- Ecosystem **major**: a milestone. The current milestones all say 1.0.
- Ecosystem **minor**: a feature set that ships across several apps.
- An ecosystem patch is a fix-only re-release; it re-pins the apps that changed.
- The ecosystem number is not derived from the app numbers. A fix in one app does not bump it.
- An app stays `0.x` until it ships inside an ecosystem release that calls it stable.
- A breaking signal change bumps the schema major and the cynthus-shared major, and forces a pin
  bump in every service.

## Rules for a manifest

1. Pin tags, never branches.
2. Record the signal schema version and the API contract version.
3. A manifest marked `Draft` may change; a `Released` manifest is never edited, only superseded.
4. Every app listed has a `CHANGELOG.md` section for the pinned version.

## Releases

- [1.0 (draft)](1.0.md)
