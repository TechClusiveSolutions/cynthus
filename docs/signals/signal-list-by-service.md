# Signals by service

**Version:** 1.0 (2026-11-03)  
**Generated from:** `signal-catalog.md` v1.0 (204 signals with a publisher and consumers; 35 more features are synchronous or in-process and publish nothing). The tables are derived from the catalog: when the catalog changes, update them to match.  
**Supersedes:** `signal-handling-matrix.md` (2026-06-01, topic-level), now in `archive/signals/`.

## How to read this

- *Publishes* lists each signal the service emits, its topic, and who consumes it.
- *Consumes* lists each signal the service receives and who publishes it. `cynthus-audit` and `cynthus-notification` consume a large share of all signals, so they are summarised by domain.
- A service with no signals either has none yet (stubs, emulators, caches, databases) or is not named in the catalog.

## Summary

- `cynthus-core-api`
  - Publishes: 69
  - Consumes: 29
- `cynthus-core-cache`
  - Publishes: 1
  - Consumes: 10
- `cynthus-inventory`
  - Publishes: 19
  - Consumes: 5
- `cynthus-recipe`
  - Publishes: 15
  - Consumes: 8
- `cynthus-profile`
  - Publishes: 13
  - Consumes: 3
- `cynthus-shopping`
  - Publishes: 22
  - Consumes: 4
- `cynthus-scheduler`
  - Publishes: 9
  - Consumes: 13
- `cynthus-worker`
  - Publishes: 11
  - Consumes: 7
- `cynthus-notification`
  - Publishes: 0
  - Consumes: 41
- `cynthus-identity`
  - Publishes: 3
  - Consumes: 13
- `cynthus-audit`
  - Publishes: 1
  - Consumes: 152
- `cynthus-chat`
  - Publishes: 10
  - Consumes: 35
- `cynthus-analysis`
  - Publishes: 7
  - Consumes: 20
- `cynthus-video`
  - Publishes: 4
  - Consumes: 0
- `cynthus-health-api`
  - Publishes: 5
  - Consumes: 2
- `cynthus-messaging` (catalog name; not a service)
  - Publishes: 4
  - Consumes: 5
- `cynthus-billing-api`
  - Publishes: 4
  - Consumes: 5
- `cynthus-partner-api`
  - Publishes: 11
  - Consumes: 9
- `spire-agent`
  - Publishes: 2
  - Consumes: 0
- `spire-server`
  - Publishes: 1
  - Consumes: 0

## Cynthus Core (open source)

### `cynthus-core-api`

Primary edge for user interactions; context assembly.

**Publishes (69 signals)**

- `public.shopping_list.list.requested`
  - Topic: public
  - Consumers: `cynthus-shopping`
- `public.meal.suggestion.requested`
  - Topic: public
  - Consumers: `cynthus-chat`, `cynthus-audit`
- `public.meal.suggestion.accepted`
  - Topic: public
  - Consumers: `cynthus-chat`, `cynthus-analysis`, `cynthus-audit`
- `public.meal.suggestion.denied`
  - Topic: public
  - Consumers: `cynthus-chat`, `cynthus-analysis`, `cynthus-audit`
- `internal.meal.suggestion_schedule.configured`
  - Topic: internal
  - Consumers: `cynthus-scheduler`
- `public.meal.plan.created`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-scheduler`, `cynthus-audit`
- `public.meal.plan.updated`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-scheduler`, `cynthus-audit`
- `public.meal.plan.deleted`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-scheduler`, `cynthus-audit`
- `public.meal.recipes.associated`
  - Topic: public
  - Consumers: `cynthus-recipe`, `cynthus-analysis`, `cynthus-audit`
- `public.meal.vote.initiated`
  - Topic: public
  - Consumers: `cynthus-messaging`, `cynthus-notification`, `cynthus-audit`
- `public.meal.vote.cast`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-messaging`, `cynthus-audit`
- `public.meal.vote.resolved`
  - Topic: public
  - Consumers: `cynthus-chat`, `cynthus-notification`, `cynthus-audit`
- `audit.inventory.location.role_assigned`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.inventory.location.role_revoked`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `internal.inventory.location.subscription_created`
  - Topic: internal
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `internal.inventory.location.subscription_removed`
  - Topic: internal
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.inventory.order.initiated`
  - Topic: public
  - Consumers: `cynthus-partner-api`, `cynthus-billing-api`, `cynthus-audit`
- `internal.inventory.scan.receipt_submitted`
  - Topic: internal
  - Consumers: `cynthus-worker`
- `public.inventory.mutation.recorded`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-audit`
- `public.recipe.substitution.requested`
  - Topic: public
  - Consumers: `cynthus-chat`, `cynthus-audit`
- `internal.shopping_list.generation.requested`
  - Topic: internal
  - Consumers: `cynthus-chat`
- `public.group.created`
  - Topic: public
  - Consumers: `cynthus-identity`, `cynthus-audit`
- `public.group.updated`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.group.deleted`
  - Topic: public
  - Consumers: `cynthus-identity`, `cynthus-messaging`, `cynthus-audit`
- `public.group.member_added`
  - Topic: public
  - Consumers: `cynthus-identity`, `cynthus-notification`, `cynthus-audit`
- `public.group.member_role_changed`
  - Topic: public
  - Consumers: `cynthus-identity`, `cynthus-audit`
- `public.group.member_removed`
  - Topic: public
  - Consumers: `cynthus-identity`, `cynthus-notification`, `cynthus-audit`
- `public.group.join_requested`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.group.join_approved`
  - Topic: public
  - Consumers: `cynthus-identity`, `cynthus-notification`, `cynthus-audit`
- `public.engagement.created`
  - Topic: public
  - Consumers: `cynthus-chat`, `cynthus-notification`, `cynthus-audit`
- `public.engagement.updated`
  - Topic: public
  - Consumers: `cynthus-chat`, `cynthus-notification`, `cynthus-audit`
- `public.engagement.deleted`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.engagement.attendee_joined`
  - Topic: public
  - Consumers: `cynthus-chat`, `cynthus-profile`, `cynthus-audit`
- `public.engagement.attendee_declined`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `audit.engagement.manager_assigned`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `public.live_session.started`
  - Topic: public
  - Consumers: `cynthus-messaging`, `cynthus-audit`
- `public.live_session.ended`
  - Topic: public
  - Consumers: `cynthus-audit`
- `internal.intelligence.chat.session_started`
  - Topic: internal
  - Consumers: `cynthus-chat`, `cynthus-audit`
- `internal.intelligence.context.assembled`
  - Topic: internal
  - Consumers: `cynthus-chat`
- `internal.intelligence.chat.message_requested`
  - Topic: internal
  - Consumers: `cynthus-chat`
- `public.vendor.subscription_created`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-partner-api`, `cynthus-chat`, `cynthus-audit`
- `public.vendor.subscription_removed`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-partner-api`, `cynthus-audit`
- `internal.vendor_directory.search.performed`
  - Topic: internal
  - Consumers: `cynthus-partner-api`
- `audit.account.contact_updated`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.account.business_profile_updated`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `internal.account.deletion_requested`
  - Topic: internal
  - Consumers: `cynthus-scheduler`, `cynthus-audit`
- `internal.account.onboarding_started`
  - Topic: internal
  - Consumers: `cynthus-audit`
- `internal.account.onboarding_completed`
  - Topic: internal
  - Consumers: `cynthus-chat`, `cynthus-audit`
- `public.rating.created`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-chat`, `cynthus-audit`
- `public.rating.updated`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-audit`
- `internal.tag.created`
  - Topic: internal
  - Consumers: `cynthus-audit`
- `internal.tag.assigned`
  - Topic: internal
  - Consumers: `cynthus-analysis`, `cynthus-audit`
- `internal.tag.removed`
  - Topic: internal
  - Consumers: `cynthus-audit`
- `public.access.request.submitted`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.access.request.approved`
  - Topic: public
  - Consumers: `cynthus-identity`, `cynthus-notification`, `cynthus-audit`
- `public.access.request.denied`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `internal.data_export.requested`
  - Topic: internal
  - Consumers: `cynthus-worker`
- `internal.worker.job.queued`
  - Topic: internal
  - Consumers: `cynthus-worker`
- `audit.identity.token_exchanged`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.identity.token_exchange_failed`
  - Topic: audit
  - Consumers: `cynthus-audit`, `cynthus-notification`
- `audit.identity.access.granted`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.identity.access.rejected`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.identity.access.denied`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `public.inventory.location.requested`
  - Topic: public
  - Consumers: `cynthus-inventory`, `cynthus-audit`
- `public.inventory.shelf.requested`
  - Topic: public
  - Consumers: `cynthus-inventory`, `cynthus-audit`
- `public.inventory.item.requested`
  - Topic: public
  - Consumers: `cynthus-inventory`, `cynthus-audit`
- `public.inventory.owner.requested`
  - Topic: public
  - Consumers: `cynthus-inventory`, `cynthus-audit`
- `public.inventory.list.requested`
  - Topic: public
  - Consumers: `cynthus-inventory`, `cynthus-audit`
- `public.profile.profile.requested`
  - Topic: public
  - Consumers: `cynthus-profile`, `cynthus-audit`

**Consumes (29 signals)**

- `public.shopping_list.list.responded`: `cynthus-shopping`
- `public.meal.suggestion.generated`: `cynthus-chat`
- `internal.meal.suggestion_schedule.triggered`: `cynthus-scheduler`
- `public.meal.vote.auto_resolved`: `cynthus-chat`
- `internal.profile.energy_level.updated`: `cynthus-profile`
- `internal.inventory.scan.completed`: `cynthus-worker`
- `internal.inventory.item.prioritized_for_expiry`: `cynthus-scheduler`
- `public.recipe.created`: `cynthus-recipe`
- `public.recipe.updated`: `cynthus-recipe`
- `public.recipe.deleted`: `cynthus-recipe`
- `public.recipe.scaled`: `cynthus-recipe`
- `internal.recipe.pricing.updated`: `cynthus-recipe`
- `public.recipe.variant.saved`: `cynthus-recipe`
- `internal.shopping_list.procurement_target.set`: `cynthus-shopping`
- `internal.intelligence.chat.session_ended`: `cynthus-chat`
- `internal.intelligence.chat.interaction_recorded`: `cynthus-chat`
- `internal.intelligence.chat.message_generated`: `cynthus-chat`
- `internal.account.deletion_confirmed`: `cynthus-scheduler`
- `internal.profile.accessibility_preference.updated`: `cynthus-profile`
- `internal.profile.locale.updated`: `cynthus-profile`
- `internal.analysis.harmony_score.computed`: `cynthus-analysis`
- `internal.analytics.spend.snapshot_recorded`: `cynthus-analysis`
- `internal.cache.sync.invalidated`: `cynthus-core-cache`
- `public.inventory.location.responded`: `cynthus-inventory`
- `public.inventory.shelf.responded`: `cynthus-inventory`
- `public.inventory.item.responded`: `cynthus-inventory`
- `public.inventory.owner.responded`: `cynthus-inventory`
- `public.inventory.list.updated`: `cynthus-inventory`
- `public.profile.profile.responded`: `cynthus-profile`

### `cynthus-core-web`

UI renderer for user interactions.

No signals in the catalog.

### `cynthus-core-cache`

Caching for core services.

**Publishes (1 signal)**

- `internal.cache.sync.invalidated`
  - Topic: internal
  - Consumers: `cynthus-core-api`

**Consumes (10 signals)**

- `public.inventory.location.created`: `cynthus-inventory`
- `public.inventory.location.updated`: `cynthus-inventory`
- `public.inventory.location.deleted`: `cynthus-inventory`
- `public.inventory.shelf.created`: `cynthus-inventory`
- `public.inventory.shelf.updated`: `cynthus-inventory`
- `public.inventory.shelf.deleted`: `cynthus-inventory`
- `public.inventory.item.added`: `cynthus-inventory`
- `public.inventory.item.updated`: `cynthus-inventory`
- `public.inventory.item.removed`: `cynthus-inventory`
- `public.inventory.mutation.recorded`: `cynthus-core-api`

### `cynthus-core-db`

Persistent storage for core services (clustered, one schema per service).

No signals in the catalog.

### `cynthus-inventory`

Inventory management.

**Publishes (19 signals)**

- `public.inventory.location.created`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-audit`
- `public.inventory.location.updated`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-audit`
- `public.inventory.location.deleted`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-shopping`, `cynthus-audit`
- `public.inventory.shelf.created`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-audit`
- `public.inventory.shelf.updated`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-audit`
- `public.inventory.shelf.deleted`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-audit`
- `public.inventory.item.added`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-scheduler`, `cynthus-audit`
- `public.inventory.item.updated`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-scheduler`, `cynthus-audit`
- `public.inventory.item.removed`
  - Topic: public
  - Consumers: `cynthus-core-cache`, `cynthus-scheduler`, `cynthus-audit`
- `public.inventory.owner.added`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.inventory.owner.removed`
  - Topic: public
  - Consumers: `cynthus-audit`
- `audit.identity.access.granted`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.identity.access.rejected`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.identity.access.denied`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `public.inventory.location.responded`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-audit`
- `public.inventory.shelf.responded`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-audit`
- `public.inventory.item.responded`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-audit`
- `public.inventory.owner.responded`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-audit`
- `public.inventory.list.updated`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-audit`

**Consumes (5 signals)**

- `public.inventory.location.requested`: `cynthus-core-api`
- `public.inventory.shelf.requested`: `cynthus-core-api`
- `public.inventory.item.requested`: `cynthus-core-api`
- `public.inventory.owner.requested`: `cynthus-core-api`
- `public.inventory.list.requested`: `cynthus-core-api`

### `cynthus-recipe`

Recipe ingestion and storage.

**Publishes (15 signals)**

- `public.recipe.library.created`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.recipe.library.updated`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.recipe.library.deleted`
  - Topic: public
  - Consumers: `cynthus-audit`
- `audit.recipe.library.role_assigned`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.recipe.library.role_revoked`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `public.recipe.created`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-analysis`, `cynthus-audit`
- `public.recipe.updated`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-analysis`, `cynthus-audit`
- `public.recipe.deleted`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-audit`
- `internal.recipe.import.url_submitted`
  - Topic: internal
  - Consumers: `cynthus-worker`
- `public.recipe.scaled`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-analysis`, `cynthus-audit`
- `internal.recipe.pricing.updated`
  - Topic: internal
  - Consumers: `cynthus-core-api`
- `internal.recipe.ocr.image_submitted`
  - Topic: internal
  - Consumers: `cynthus-worker`
- `internal.recipe.scrape.url_submitted`
  - Topic: internal
  - Consumers: `cynthus-worker`
- `public.recipe.variant.saved`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-audit`
- `internal.worker.job.queued`
  - Topic: internal
  - Consumers: `cynthus-worker`

**Consumes (8 signals)**

- `public.meal.recipes.associated`: `cynthus-core-api`
- `internal.recipe.import.completed`: `cynthus-worker`
- `internal.recipe.import.failed`: `cynthus-worker`
- `internal.recipe.modification.clinically_suggested`: `cynthus-chat`
- `internal.recipe.ocr.completed`: `cynthus-worker`
- `internal.recipe.scrape.completed`: `cynthus-worker`
- `internal.recipe.nutrition.enriched`: `cynthus-worker`
- `public.recipe.substitution.suggested`: `cynthus-chat`

### `cynthus-logistics`

Inventory logistics (movement between locations, ordering, delivery).

No signals in the catalog.

### `cynthus-profile`

Preferences and hard constraints.

**Publishes (13 signals)**

- `internal.profile.energy_level.updated`
  - Topic: internal
  - Consumers: `cynthus-chat`, `cynthus-core-api`
- `internal.profile.soft_preferences.updated`
  - Topic: internal
  - Consumers: `cynthus-chat`, `cynthus-audit`
- `audit.profile.hard_constraint.updated`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `internal.profile.notification_preferences.updated`
  - Topic: internal
  - Consumers: `cynthus-notification`, `cynthus-scheduler`
- `internal.profile.favorite.added`
  - Topic: internal
  - Consumers: `cynthus-chat`, `cynthus-analysis`
- `internal.profile.favorite.removed`
  - Topic: internal
  - Consumers: `cynthus-chat`, `cynthus-analysis`
- `internal.profile.accessibility_preference.updated`
  - Topic: internal
  - Consumers: `cynthus-chat`, `cynthus-core-api`
- `internal.profile.locale.updated`
  - Topic: internal
  - Consumers: `cynthus-core-api`, `cynthus-chat`
- `public.profile.profile.responded`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-audit`
- `public.profile.profile.created`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.profile.profile.updated`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.profile.profile.deleted`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.profile.snapshot.published`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-audit`

**Consumes (3 signals)**

- `public.engagement.attendee_joined`: `cynthus-core-api`
- `public.profile.profile.requested`: `cynthus-core-api`
- `audit.identity.user.authenticated`: `cynthus-identity`

### `cynthus-shopping`

Shopping lists (named in the catalog and the code, not in ADD 6.0).

**Publishes (22 signals)**

The first three signals are implemented as `public.shopping_list.list.created`, `.updated` and `.deleted`; see the catalog's "Implemented names" table.

- `public.shopping_list.list.responded`
  - Topic: public
  - Consumers: `cynthus-core-api`
- `public.shopping_list.created`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.shopping_list.updated`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.shopping_list.deleted`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.shopping_list.item.added`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-audit`
- `public.shopping_list.item.updated`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-audit`
- `public.shopping_list.item.checked_off`
  - Topic: public
  - Consumers: `cynthus-analysis`, `cynthus-audit`
- `public.shopping_list.item.removed`
  - Topic: public
  - Consumers: `cynthus-audit`
- `audit.shopping_list.role_assigned`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.shopping_list.role_revoked`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `internal.shopping_list.procurement_target.set`
  - Topic: internal
  - Consumers: `cynthus-core-api`, `cynthus-scheduler`
- `internal.shopping_list.item.vendor_preference_set`
  - Topic: internal
  - Consumers: `cynthus-chat`, `cynthus-partner-api`
- `audit.shopping_list.management_delegated`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.shopping_list.management_revoked`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `public.shopping_list.access_requested`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.shopping_list.access_request_withdrawn`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.shopping_list.access_granted`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-identity`, `cynthus-audit`
- `public.shopping_list.access_denied`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `internal.shopping_list.autopurchase.schedule_configured`
  - Topic: internal
  - Consumers: `cynthus-scheduler`
- `public.shopping_list.autopurchase.confirmed`
  - Topic: public
  - Consumers: `cynthus-partner-api`, `cynthus-billing-api`, `cynthus-audit`
- `public.shopping_list.autopurchase.cancelled`
  - Topic: public
  - Consumers: `cynthus-scheduler`, `cynthus-audit`
- `public.shopping_list.autopurchase.modified`
  - Topic: public
  - Consumers: `cynthus-scheduler`, `cynthus-audit`

**Consumes (4 signals)**

- `public.shopping_list.list.requested`: `cynthus-core-api`
- `public.inventory.location.deleted`: `cynthus-inventory`
- `public.inventory.item.low`: `cynthus-scheduler`
- `internal.shopping_list.generation.completed`: `cynthus-chat`

### `cynthus-scheduler`

Periodic time-based task management.

**Publishes (9 signals)**

- `internal.meal.suggestion_schedule.triggered`
  - Topic: internal
  - Consumers: `cynthus-core-api`
- `public.inventory.item.low`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-chat`, `cynthus-shopping`, `cynthus-audit`
- `public.inventory.item.expiry_approaching`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-chat`, `cynthus-analysis`, `cynthus-audit`
- `public.inventory.item.expired`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-chat`, `cynthus-audit`
- `internal.inventory.item.prioritized_for_expiry`
  - Topic: internal
  - Consumers: `cynthus-core-api`
- `internal.shopping_list.autopurchase.reminder_due`
  - Topic: internal
  - Consumers: `cynthus-notification`, `cynthus-chat`
- `internal.shopping_list.meal_gap.detected`
  - Topic: internal
  - Consumers: `cynthus-notification`, `cynthus-chat`
- `public.promotion.expired`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-partner-api`, `cynthus-audit`
- `internal.account.deletion_confirmed`
  - Topic: internal
  - Consumers: `cynthus-core-api`, `cynthus-worker`, `cynthus-audit`

**Consumes (13 signals)**

- `internal.meal.suggestion_schedule.configured`: `cynthus-core-api`
- `public.meal.plan.created`: `cynthus-core-api`
- `public.meal.plan.updated`: `cynthus-core-api`
- `public.meal.plan.deleted`: `cynthus-core-api`
- `public.inventory.item.added`: `cynthus-inventory`
- `public.inventory.item.updated`: `cynthus-inventory`
- `public.inventory.item.removed`: `cynthus-inventory`
- `internal.shopping_list.procurement_target.set`: `cynthus-shopping`
- `internal.shopping_list.autopurchase.schedule_configured`: `cynthus-shopping`
- `public.shopping_list.autopurchase.cancelled`: `cynthus-shopping`
- `public.shopping_list.autopurchase.modified`: `cynthus-shopping`
- `internal.account.deletion_requested`: `cynthus-core-api`
- `internal.profile.notification_preferences.updated`: `cynthus-profile`

### `cynthus-worker`

Ingress and non-time-based task management.

**Publishes (11 signals)**

- `internal.inventory.scan.completed`
  - Topic: internal
  - Consumers: `cynthus-core-api`
- `internal.recipe.import.completed`
  - Topic: internal
  - Consumers: `cynthus-recipe`
- `internal.recipe.import.failed`
  - Topic: internal
  - Consumers: `cynthus-recipe`, `cynthus-notification`
- `internal.recipe.ocr.completed`
  - Topic: internal
  - Consumers: `cynthus-recipe`
- `internal.recipe.scrape.completed`
  - Topic: internal
  - Consumers: `cynthus-recipe`
- `internal.recipe.nutrition.enriched`
  - Topic: internal
  - Consumers: `cynthus-recipe`
- `audit.account.data_erased`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `internal.data_export.completed`
  - Topic: internal
  - Consumers: `cynthus-notification`
- `internal.worker.job.queued`
  - Topic: internal
  - Consumers: `cynthus-worker`
- `internal.worker.job.completed`
  - Topic: internal
  - Consumers: none
- `internal.worker.job.failed`
  - Topic: internal
  - Consumers: `cynthus-notification`

**Consumes (7 signals)**

- `internal.inventory.scan.receipt_submitted`: `cynthus-core-api`
- `internal.recipe.import.url_submitted`: `cynthus-recipe`
- `internal.recipe.ocr.image_submitted`: `cynthus-recipe`
- `internal.recipe.scrape.url_submitted`: `cynthus-recipe`
- `internal.account.deletion_confirmed`: `cynthus-scheduler`
- `internal.data_export.requested`: `cynthus-core-api`
- `internal.worker.job.queued`: `cynthus-core-api`, `cynthus-recipe`, `cynthus-worker`

### `cynthus-messaging-engine`

Real-time WebSocket hub for group chat (the catalog calls its consumer `cynthus-messaging`).

No signals in the catalog.

### `cynthus-notification`

Notifications (named in the catalog, not in ADD 6.0).

**Consumes (41 signals)**, by domain: Access Control 3; Account Management 1; Clinical Monitoring 1; Data Analytics and Dashboards 1; Engagement Management 4; Group Management 4; Inventory Management 7; Meal Planning 4; Messaging 1; Platform Infrastructure 1; Recipe Management 1; Reporting and Compliance 1; Security and Identity 1; Service and Resource Management 5; Shopping List 6.

## Cynthus Trust (closed source)

### `cynthus-identity`

Identity management and authentication.

**Publishes (3 signals)**

- `audit.identity.user.authenticated`
  - Topic: audit
  - Consumers: `cynthus-audit`, `cynthus-profile`
- `audit.identity.user.rejected`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `audit.identity.token.issued`
  - Topic: audit
  - Consumers: `cynthus-audit`

**Consumes (13 signals)**

- `public.shopping_list.access_granted`: `cynthus-shopping`
- `public.group.created`: `cynthus-core-api`
- `public.group.deleted`: `cynthus-core-api`
- `public.group.member_added`: `cynthus-core-api`
- `public.group.member_role_changed`: `cynthus-core-api`
- `public.group.member_removed`: `cynthus-core-api`
- `public.group.join_approved`: `cynthus-core-api`
- `internal.system.subscription.upgraded`: `cynthus-billing-api`
- `internal.system.subscription.downgraded`: `cynthus-billing-api`
- `internal.system.entitlement.updated`: `cynthus-billing-api`
- `audit.access.provider_data_consent_granted`: `cynthus-health-api`
- `audit.access.provider_data_consent_revoked`: `cynthus-health-api`
- `public.access.request.approved`: `cynthus-core-api`

### `cynthus-audit`

Auditing and compliance.

**Publishes (1 signal)**

- `audit.system.ledger.entry_written`
  - Topic: audit
  - Consumers: none

**Consumes (152 signals)**, by domain: AI Companion 4; Access Control 5; Account Management 15; Billing Management 3; Clinical Monitoring 5; Contribution Management 1; Engagement Management 6; Group Management 8; Inventory Management 29; Live Companion 2; Meal Planning 12; Messaging 4; Rating Management 2; Recipe Management 13; Security and Identity 11; Service and Resource Management 11; Shopping List 18; Tag Management 3.

### `cynthus-trust-cache`

Caching for trust services.

No signals in the catalog.

### `cynthus-trust-db`

Persistent storage for trust services.

No signals in the catalog.

## Cynthus Intelligence (closed source)

### `cynthus-chat`

Astri persona (conversational life assistant and companion).

**Publishes (10 signals)**

- `public.meal.suggestion.generated`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-notification`, `cynthus-audit`
- `public.meal.vote.auto_resolved`
  - Topic: public
  - Consumers: `cynthus-core-api`, `cynthus-notification`, `cynthus-audit`
- `internal.recipe.modification.clinically_suggested`
  - Topic: internal
  - Consumers: `cynthus-recipe`, `cynthus-audit`
- `public.recipe.substitution.suggested`
  - Topic: public
  - Consumers: `cynthus-recipe`, `cynthus-audit`
- `internal.shopping_list.generation.completed`
  - Topic: internal
  - Consumers: `cynthus-shopping`
- `internal.shopping_list.promotional_data.requested`
  - Topic: internal
  - Consumers: `cynthus-partner-api`
- `internal.live_session.step_advanced`
  - Topic: internal
  - Consumers: `cynthus-messaging`
- `internal.intelligence.chat.session_ended`
  - Topic: internal
  - Consumers: `cynthus-core-api`, `cynthus-audit`
- `internal.intelligence.chat.interaction_recorded`
  - Topic: internal
  - Consumers: `cynthus-core-api`, `cynthus-audit`
- `internal.intelligence.chat.message_generated`
  - Topic: internal
  - Consumers: `cynthus-core-api`, `cynthus-audit`

**Consumes (35 signals)**, by domain: AI Companion 3; Accessibility 4; Account Management 2; Clinical Monitoring 2; Engagement Management 3; Inventory Management 3; Meal Planning 6; Platform Infrastructure 2; Rating Management 3; Recipe Management 1; Service and Resource Management 2; Shopping List 4.

### `cynthus-analysis`

Sentiment, biometric trend, energy level and dietary trend analysis.

**Publishes (7 signals)**

- `internal.meal.vote.stalemate_detected`
  - Topic: internal
  - Consumers: `cynthus-chat`
- `internal.health.telemetry.snapshot_recorded`
  - Topic: internal
  - Consumers: `cynthus-audit`
- `public.health.biometric.anomaly_detected`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-chat`, `cynthus-health-api`, `cynthus-audit`
- `internal.health.analysis.correlation_completed`
  - Topic: internal
  - Consumers: `cynthus-chat`, `cynthus-health-api`
- `internal.analysis.harmony_score.computed`
  - Topic: internal
  - Consumers: `cynthus-core-api`, `cynthus-notification`
- `internal.analytics.spend.snapshot_recorded`
  - Topic: internal
  - Consumers: `cynthus-core-api`
- `internal.analytics.trend.computed`
  - Topic: internal
  - Consumers: `cynthus-partner-api`

**Consumes (20 signals)**

- `public.meal.suggestion.accepted`: `cynthus-core-api`
- `public.meal.suggestion.denied`: `cynthus-core-api`
- `public.meal.plan.created`: `cynthus-core-api`
- `public.meal.plan.updated`: `cynthus-core-api`
- `public.meal.plan.deleted`: `cynthus-core-api`
- `public.meal.recipes.associated`: `cynthus-core-api`
- `public.meal.vote.cast`: `cynthus-core-api`
- `public.inventory.item.expiry_approaching`: `cynthus-scheduler`
- `public.recipe.created`: `cynthus-recipe`
- `public.recipe.updated`: `cynthus-recipe`
- `public.recipe.scaled`: `cynthus-recipe`
- `public.shopping_list.item.added`: `cynthus-shopping`
- `public.shopping_list.item.updated`: `cynthus-shopping`
- `public.shopping_list.item.checked_off`: `cynthus-shopping`
- `public.rating.created`: `cynthus-core-api`
- `public.rating.updated`: `cynthus-core-api`
- `internal.profile.favorite.added`: `cynthus-profile`
- `internal.profile.favorite.removed`: `cynthus-profile`
- `internal.tag.assigned`: `cynthus-core-api`
- `public.profile.snapshot.published`: `cynthus-profile`

### `cynthus-video`

Heads-up display and real-time video for live and AI companion mode.

**Publishes (4 signals)**

- `internal.spatial.object_detected`
  - Topic: internal
  - Consumers: `cynthus-chat`
- `internal.spatial.frame_processed`
  - Topic: internal
  - Consumers: `cynthus-chat`
- `internal.spatial.object_detected`
  - Topic: internal
  - Consumers: `cynthus-chat`
- `internal.spatial.frame_processed`
  - Topic: internal
  - Consumers: `cynthus-chat`

### `cynthus-intel-cache`

Caching for intelligence services.

No signals in the catalog.

### `cynthus-intel-db`

Persistent storage for intelligence services.

No signals in the catalog.

## Cynthus Health (closed source)

### `cynthus-health-api`

Primary edge for clinical integrations.

**Publishes (5 signals)**

- `audit.health.provider_data_access`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `internal.health.rpm.transmission_logged`
  - Topic: internal
  - Consumers: `cynthus-billing-api`, `cynthus-audit`
- `internal.health.rpm.clinician_interaction_logged`
  - Topic: internal
  - Consumers: `cynthus-billing-api`, `cynthus-audit`
- `audit.access.provider_data_consent_granted`
  - Topic: audit
  - Consumers: `cynthus-audit`, `cynthus-identity`
- `audit.access.provider_data_consent_revoked`
  - Topic: audit
  - Consumers: `cynthus-audit`, `cynthus-identity`

**Consumes (2 signals)**

- `public.health.biometric.anomaly_detected`: `cynthus-analysis`
- `internal.health.analysis.correlation_completed`: `cynthus-analysis`

### `cynthus-health-web`

UI renderer for clinical interactions.

No signals in the catalog.

### `cynthus-device`

Device telemetry aggregator (provisional: expected in the `cynthus-health` repository; HUD and video data may need a different home). No signals in the catalog.

### `cynthus-messaging` (catalog name; not a service)

The catalog uses this name for the group-chat component (FT-MS-001 to 003). `cynthus-messaging` is the private communication library, not a service, so these signals have no owner yet. See the discrepancies below.

**Publishes (4 signals)**

- `public.messaging.message.sent`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.messaging.message.deleted`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.messaging.recipe.shared`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.messaging.inventory_item.shared`
  - Topic: public
  - Consumers: `cynthus-audit`

**Consumes (5 signals)**

- `public.meal.vote.initiated`: `cynthus-core-api`
- `public.meal.vote.cast`: `cynthus-core-api`
- `public.group.deleted`: `cynthus-core-api`
- `public.live_session.started`: `cynthus-core-api`
- `internal.live_session.step_advanced`: `cynthus-chat`

### `cynthus-health-cache`

Caching for health services.

No signals in the catalog.

### `cynthus-health-db`

Persistent storage for health services.

No signals in the catalog.

## Cynthus Commerce (closed source)

### `cynthus-billing-api`

Subscriptions, booster packs, tier enforcement.

**Publishes (4 signals)**

- `internal.system.payment_method.updated`
  - Topic: internal
  - Consumers: `cynthus-audit`
- `internal.system.subscription.upgraded`
  - Topic: internal
  - Consumers: `cynthus-identity`, `cynthus-audit`
- `internal.system.subscription.downgraded`
  - Topic: internal
  - Consumers: `cynthus-identity`, `cynthus-audit`
- `internal.system.entitlement.updated`
  - Topic: internal
  - Consumers: `cynthus-identity`

**Consumes (5 signals)**

- `public.inventory.order.initiated`: `cynthus-core-api`
- `public.shopping_list.autopurchase.confirmed`: `cynthus-shopping`
- `internal.health.rpm.transmission_logged`: `cynthus-health-api`
- `internal.health.rpm.clinician_interaction_logged`: `cynthus-health-api`
- `audit.partner.contribution_recorded`: `cynthus-partner-api`

### `cynthus-partner-api`

Partner integrations.

**Publishes (11 signals)**

- `public.inventory.order.submitted`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.inventory.order.failed`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.service_registry.created`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.service_registry.updated`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.service_registry.deleted`
  - Topic: public
  - Consumers: `cynthus-audit`
- `audit.service_registry.management_delegated`
  - Topic: audit
  - Consumers: `cynthus-audit`
- `public.promotion.created`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-chat`, `cynthus-audit`
- `public.promotion.updated`
  - Topic: public
  - Consumers: `cynthus-notification`, `cynthus-audit`
- `public.device_registry.device_listed`
  - Topic: public
  - Consumers: `cynthus-audit`
- `public.device_registry.device_removed`
  - Topic: public
  - Consumers: `cynthus-audit`
- `audit.partner.contribution_recorded`
  - Topic: audit
  - Consumers: `cynthus-audit`, `cynthus-billing-api`

**Consumes (9 signals)**

- `public.inventory.order.initiated`: `cynthus-core-api`
- `internal.shopping_list.item.vendor_preference_set`: `cynthus-shopping`
- `internal.shopping_list.promotional_data.requested`: `cynthus-chat`
- `public.shopping_list.autopurchase.confirmed`: `cynthus-shopping`
- `public.promotion.expired`: `cynthus-scheduler`
- `public.vendor.subscription_created`: `cynthus-core-api`
- `public.vendor.subscription_removed`: `cynthus-core-api`
- `internal.vendor_directory.search.performed`: `cynthus-core-api`
- `internal.analytics.trend.computed`: `cynthus-analysis`

### `cynthus-comm-web`

UI renderer for partner, supplier and provider interactions.

No signals in the catalog.

### `cynthus-comm-cache`

Caching for commerce services.

No signals in the catalog.

### `cynthus-comm-db`

Persistent storage for commerce services.

No signals in the catalog.

## Cynthus Emulators

### `cynthus-signal-bus`

Azure Service Bus emulator.

No signals in the catalog.

### `cynthus-signal-db`

MS SQL storage for the Service Bus emulator.

No signals in the catalog.

## Workload identity (SPIFFE/SPIRE)

### `spire-agent`

Issues and rotates workload SVIDs.

**Publishes (2 signals)**

- `internal.identity.svid.issued`
  - Topic: internal
  - Consumers: `cynthus-audit`
- `internal.identity.svid.rotated`
  - Topic: internal
  - Consumers: `cynthus-audit`

### `spire-server`

Revokes SVIDs.

**Publishes (1 signal)**

- `audit.identity.svid.revoked`
  - Topic: audit
  - Consumers: `cynthus-audit`

## Discrepancies found while generating this list

These are for the document owner to decide. Nothing here has been changed in the catalog or ADD 6.0.

1. **`cynthus-shopping` and `cynthus-notification`** are publishers or consumers in the catalog (21 and 41 signals) but are not in the ADD 6.0 service tables. `cynthus-shopping` also exists as a container in the `cynthus-core` repository.
2. **`cynthus-messaging` is a library, not a service** (owner, 2026-11-03). The catalog still uses it as publisher or consumer of the group-chat signals (FT-MS-001 to 003, vote, group and live-session signals: 12 rows). ADD 6.0 names a `cynthus-messaging-engine` WebSocket hub for group chat, which may contradict the rule that no service relays messages between services. Who publishes and consumes group-chat signals is undecided. The device telemetry aggregator is now `cynthus-device`.
3. **`cynthus-inventory` and `cynthus-logistics`** are in ADD 6.0 but publish nothing in the catalog. Inventory signals are published by `cynthus-core-api` (13), `cynthus-scheduler` (4), `cynthus-partner-api` (2) and `cynthus-worker` (1). The older handling matrix had `cynthus-inventory` publishing the inventory topic.
4. **`cynthus-identity`** publishes nothing in the catalog (13 signals consumed). The older matrix had it publishing the Auth and System topics. The SVID signals are published by `spire-agent` and `spire-server`, which are not in ADD 6.0.
5. **Cache and database services, `cynthus-core-web`, `cynthus-health-web`** have no signals, as expected for stores and renderers.
