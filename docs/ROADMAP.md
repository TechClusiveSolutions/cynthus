# Cynthus roadmap

**Version:** 0.1 (draft, 2026-11-03). Sources to merge: PRD section 9 (phased rollout), Feature Registry section 4
(feature summary by phase), cynthus-web NEXT-STEPS, the open items in tools/TESTING.md, and
architecture/web-app-conversion-plan.md.

## Done
- Phase 1-3 "Basic" feature prototype (`cynthus-web`, Node) - 2026-10-31
- Test suites for the Python scaffold and the Node prototype: 2058 + 64 tests, 99.0 % coverage
- Import/syntax repairs across cynthus-core, cynthus-messaging-core, cynthus-messaging (tools/FIX-LOG.md)

## Next (from existing documents, unprioritised)
- Port prototype features into the owning Python services (conversion plan)
- Resolve the TESTING.md open items: faststream.azure dependency, router/module name shadowing, scheduler
  import-time file read, half-moved payload folders, two outdated tests, folder naming
- Complete the signal-by-service list and reconcile it with the signal catalog
- Screen-reader pass (NVDA/JAWS) over the front end; WebSockets/SSE for chat
- Deployment: HTTPS, persistent volume, real session secret; rotate API keys

## Later
- Phase 4+ features: billing, tiers and boosters, supplier ordering, wearables, engagements
- Care-team sharing (Phases 7-8)
- React/Next.js renderer for `cynthus-core-web`

TODO: pull the phase dates and scope from PRD section 9 and the Registry.
