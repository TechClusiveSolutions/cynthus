# Signals by service

**Version:** 1.0 (2026-11-03)  
**Generated from:** `signal-catalog.md` v1.0 (202 signals with a publisher and consumers; 35 more features are synchronous or in-process and publish nothing). The tables are derived from the catalog: when the catalog changes, update them to match.  
**Supersedes:** `signal-handling-matrix.md` (2026-06-01, topic-level), now in `archive/signals/`.

## How to read this

- *Publishes* lists each signal the service emits, its topic, and who consumes it.
- *Consumes* lists each signal the service receives and who publishes it. `cynthus-audit` and `cynthus-notification` consume a large share of all signals, so they are summarised by domain.
- A service with no signals either has none yet (stubs, emulators, caches, databases) or is not named in the catalog.

## Summary

| Service | Publishes | Consumes |
|---|---|---|
| `cynthus-core-api` | 67 | 27 |
| `cynthus-core-cache` | 1 | 10 |
| `cynthus-inventory` | 19 | 5 |
| `cynthus-recipe` | 15 | 8 |
| `cynthus-profile` | 13 | 3 |
| `cynthus-shopping` | 21 | 3 |
| `cynthus-scheduler` | 9 | 13 |
| `cynthus-worker` | 11 | 7 |
| `cynthus-notification` | 0 | 41 |
| `cynthus-identity` | 3 | 13 |
| `cynthus-audit` | 1 | 151 |
| `cynthus-chat` | 9 | 34 |
| `cynthus-analysis` | 7 | 20 |
| `cynthus-video` | 4 | 0 |
| `cynthus-health-api` | 5 | 2 |
| `cynthus-messaging` | 4 | 5 |
| `cynthus-billing-api` | 4 | 5 |
| `cynthus-partner-api` | 11 | 9 |
| `spire-agent` | 2 | 0 |
| `spire-server` | 1 | 0 |

## Cynthus Core (open source)

### `cynthus-core-api`

Primary edge for user interactions; context assembly.

**Publishes (67 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `public.meal.suggestion.requested` | public | `cynthus-chat`, `cynthus-audit` |
| `public.meal.suggestion.accepted` | public | `cynthus-chat`, `cynthus-analysis`, `cynthus-audit` |
| `public.meal.suggestion.denied` | public | `cynthus-chat`, `cynthus-analysis`, `cynthus-audit` |
| `internal.meal.suggestion_schedule.configured` | internal | `cynthus-scheduler` |
| `public.meal.plan.created` | public | `cynthus-analysis`, `cynthus-scheduler`, `cynthus-audit` |
| `public.meal.plan.updated` | public | `cynthus-analysis`, `cynthus-scheduler`, `cynthus-audit` |
| `public.meal.plan.deleted` | public | `cynthus-analysis`, `cynthus-scheduler`, `cynthus-audit` |
| `public.meal.recipes.associated` | public | `cynthus-recipe`, `cynthus-analysis`, `cynthus-audit` |
| `public.meal.vote.initiated` | public | `cynthus-messaging`, `cynthus-notification`, `cynthus-audit` |
| `public.meal.vote.cast` | public | `cynthus-analysis`, `cynthus-messaging`, `cynthus-audit` |
| `public.meal.vote.resolved` | public | `cynthus-chat`, `cynthus-notification`, `cynthus-audit` |
| `audit.inventory.location.role_assigned` | audit | `cynthus-audit` |
| `audit.inventory.location.role_revoked` | audit | `cynthus-audit` |
| `internal.inventory.location.subscription_created` | internal | `cynthus-notification`, `cynthus-audit` |
| `internal.inventory.location.subscription_removed` | internal | `cynthus-notification`, `cynthus-audit` |
| `public.inventory.order.initiated` | public | `cynthus-partner-api`, `cynthus-billing-api`, `cynthus-audit` |
| `internal.inventory.scan.receipt_submitted` | internal | `cynthus-worker` |
| `public.inventory.mutation.recorded` | public | `cynthus-core-cache`, `cynthus-audit` |
| `public.recipe.substitution.requested` | public | `cynthus-chat`, `cynthus-audit` |
| `internal.shopping_list.generation.requested` | internal | `cynthus-chat` |
| `public.group.created` | public | `cynthus-identity`, `cynthus-audit` |
| `public.group.updated` | public | `cynthus-audit` |
| `public.group.deleted` | public | `cynthus-identity`, `cynthus-messaging`, `cynthus-audit` |
| `public.group.member_added` | public | `cynthus-identity`, `cynthus-notification`, `cynthus-audit` |
| `public.group.member_role_changed` | public | `cynthus-identity`, `cynthus-audit` |
| `public.group.member_removed` | public | `cynthus-identity`, `cynthus-notification`, `cynthus-audit` |
| `public.group.join_requested` | public | `cynthus-notification`, `cynthus-audit` |
| `public.group.join_approved` | public | `cynthus-identity`, `cynthus-notification`, `cynthus-audit` |
| `public.engagement.created` | public | `cynthus-chat`, `cynthus-notification`, `cynthus-audit` |
| `public.engagement.updated` | public | `cynthus-chat`, `cynthus-notification`, `cynthus-audit` |
| `public.engagement.deleted` | public | `cynthus-notification`, `cynthus-audit` |
| `public.engagement.attendee_joined` | public | `cynthus-chat`, `cynthus-profile`, `cynthus-audit` |
| `public.engagement.attendee_declined` | public | `cynthus-notification`, `cynthus-audit` |
| `audit.engagement.manager_assigned` | audit | `cynthus-audit` |
| `public.live_session.started` | public | `cynthus-messaging`, `cynthus-audit` |
| `public.live_session.ended` | public | `cynthus-audit` |
| `internal.intelligence.chat.session_started` | internal | `cynthus-chat`, `cynthus-audit` |
| `internal.intelligence.context.assembled` | internal | `cynthus-chat` |
| `public.vendor.subscription_created` | public | `cynthus-notification`, `cynthus-partner-api`, `cynthus-chat`, `cynthus-audit` |
| `public.vendor.subscription_removed` | public | `cynthus-notification`, `cynthus-partner-api`, `cynthus-audit` |
| `internal.vendor_directory.search.performed` | internal | `cynthus-partner-api` |
| `audit.account.contact_updated` | audit | `cynthus-audit` |
| `audit.account.business_profile_updated` | audit | `cynthus-audit` |
| `internal.account.deletion_requested` | internal | `cynthus-scheduler`, `cynthus-audit` |
| `internal.account.onboarding_started` | internal | `cynthus-audit` |
| `internal.account.onboarding_completed` | internal | `cynthus-chat`, `cynthus-audit` |
| `public.rating.created` | public | `cynthus-analysis`, `cynthus-chat`, `cynthus-audit` |
| `public.rating.updated` | public | `cynthus-analysis`, `cynthus-audit` |
| `internal.tag.created` | internal | `cynthus-audit` |
| `internal.tag.assigned` | internal | `cynthus-analysis`, `cynthus-audit` |
| `internal.tag.removed` | internal | `cynthus-audit` |
| `public.access.request.submitted` | public | `cynthus-notification`, `cynthus-audit` |
| `public.access.request.approved` | public | `cynthus-identity`, `cynthus-notification`, `cynthus-audit` |
| `public.access.request.denied` | public | `cynthus-notification`, `cynthus-audit` |
| `internal.data_export.requested` | internal | `cynthus-worker` |
| `internal.worker.job.queued` | internal | `cynthus-worker` |
| `audit.identity.token_exchanged` | audit | `cynthus-audit` |
| `audit.identity.token_exchange_failed` | audit | `cynthus-audit`, `cynthus-notification` |
| `audit.identity.access.granted` | audit | `cynthus-audit` |
| `audit.identity.access.rejected` | audit | `cynthus-audit` |
| `audit.identity.access.denied` | audit | `cynthus-audit` |
| `public.inventory.location.requested` | public | `cynthus-inventory`, `cynthus-audit` |
| `public.inventory.shelf.requested` | public | `cynthus-inventory`, `cynthus-audit` |
| `public.inventory.item.requested` | public | `cynthus-inventory`, `cynthus-audit` |
| `public.inventory.owner.requested` | public | `cynthus-inventory`, `cynthus-audit` |
| `public.inventory.list.requested` | public | `cynthus-inventory`, `cynthus-audit` |
| `public.profile.profile.requested` | public | `cynthus-profile`, `cynthus-audit` |

**Consumes (27 signals)**

| Signal | Publisher |
|---|---|
| `public.meal.suggestion.generated` | `cynthus-chat` |
| `internal.meal.suggestion_schedule.triggered` | `cynthus-scheduler` |
| `public.meal.vote.auto_resolved` | `cynthus-chat` |
| `internal.profile.energy_level.updated` | `cynthus-profile` |
| `internal.inventory.scan.completed` | `cynthus-worker` |
| `internal.inventory.item.prioritized_for_expiry` | `cynthus-scheduler` |
| `public.recipe.created` | `cynthus-recipe` |
| `public.recipe.updated` | `cynthus-recipe` |
| `public.recipe.deleted` | `cynthus-recipe` |
| `public.recipe.scaled` | `cynthus-recipe` |
| `internal.recipe.pricing.updated` | `cynthus-recipe` |
| `public.recipe.variant.saved` | `cynthus-recipe` |
| `internal.shopping_list.procurement_target.set` | `cynthus-shopping` |
| `internal.intelligence.chat.session_ended` | `cynthus-chat` |
| `internal.intelligence.chat.interaction_recorded` | `cynthus-chat` |
| `internal.account.deletion_confirmed` | `cynthus-scheduler` |
| `internal.profile.accessibility_preference.updated` | `cynthus-profile` |
| `internal.profile.locale.updated` | `cynthus-profile` |
| `internal.analysis.harmony_score.computed` | `cynthus-analysis` |
| `internal.analytics.spend.snapshot_recorded` | `cynthus-analysis` |
| `internal.cache.sync.invalidated` | `cynthus-core-cache` |
| `public.inventory.location.responded` | `cynthus-inventory` |
| `public.inventory.shelf.responded` | `cynthus-inventory` |
| `public.inventory.item.responded` | `cynthus-inventory` |
| `public.inventory.owner.responded` | `cynthus-inventory` |
| `public.inventory.list.updated` | `cynthus-inventory` |
| `public.profile.profile.responded` | `cynthus-profile` |

### `cynthus-core-web`

UI renderer for user interactions.

No signals in the catalog.

### `cynthus-core-cache`

Caching for core services.

**Publishes (1 signal)**

| Signal | Topic | Consumers |
|---|---|---|
| `internal.cache.sync.invalidated` | internal | `cynthus-core-api` |

**Consumes (10 signals)**

| Signal | Publisher |
|---|---|
| `public.inventory.location.created` | `cynthus-inventory` |
| `public.inventory.location.updated` | `cynthus-inventory` |
| `public.inventory.location.deleted` | `cynthus-inventory` |
| `public.inventory.shelf.created` | `cynthus-inventory` |
| `public.inventory.shelf.updated` | `cynthus-inventory` |
| `public.inventory.shelf.deleted` | `cynthus-inventory` |
| `public.inventory.item.added` | `cynthus-inventory` |
| `public.inventory.item.updated` | `cynthus-inventory` |
| `public.inventory.item.removed` | `cynthus-inventory` |
| `public.inventory.mutation.recorded` | `cynthus-core-api` |

### `cynthus-core-db`

Persistent storage for core services (clustered, one schema per service).

No signals in the catalog.

### `cynthus-inventory`

Inventory management.

**Publishes (19 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `public.inventory.location.created` | public | `cynthus-core-cache`, `cynthus-audit` |
| `public.inventory.location.updated` | public | `cynthus-core-cache`, `cynthus-audit` |
| `public.inventory.location.deleted` | public | `cynthus-core-cache`, `cynthus-shopping`, `cynthus-audit` |
| `public.inventory.shelf.created` | public | `cynthus-core-cache`, `cynthus-audit` |
| `public.inventory.shelf.updated` | public | `cynthus-core-cache`, `cynthus-audit` |
| `public.inventory.shelf.deleted` | public | `cynthus-core-cache`, `cynthus-audit` |
| `public.inventory.item.added` | public | `cynthus-core-cache`, `cynthus-scheduler`, `cynthus-audit` |
| `public.inventory.item.updated` | public | `cynthus-core-cache`, `cynthus-scheduler`, `cynthus-audit` |
| `public.inventory.item.removed` | public | `cynthus-core-cache`, `cynthus-scheduler`, `cynthus-audit` |
| `public.inventory.owner.added` | public | `cynthus-audit` |
| `public.inventory.owner.removed` | public | `cynthus-audit` |
| `audit.identity.access.granted` | audit | `cynthus-audit` |
| `audit.identity.access.rejected` | audit | `cynthus-audit` |
| `audit.identity.access.denied` | audit | `cynthus-audit` |
| `public.inventory.location.responded` | public | `cynthus-core-api`, `cynthus-audit` |
| `public.inventory.shelf.responded` | public | `cynthus-core-api`, `cynthus-audit` |
| `public.inventory.item.responded` | public | `cynthus-core-api`, `cynthus-audit` |
| `public.inventory.owner.responded` | public | `cynthus-core-api`, `cynthus-audit` |
| `public.inventory.list.updated` | public | `cynthus-core-api`, `cynthus-audit` |

**Consumes (5 signals)**

| Signal | Publisher |
|---|---|
| `public.inventory.location.requested` | `cynthus-core-api` |
| `public.inventory.shelf.requested` | `cynthus-core-api` |
| `public.inventory.item.requested` | `cynthus-core-api` |
| `public.inventory.owner.requested` | `cynthus-core-api` |
| `public.inventory.list.requested` | `cynthus-core-api` |

### `cynthus-recipe`

Recipe ingestion and storage.

**Publishes (15 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `public.recipe.library.created` | public | `cynthus-audit` |
| `public.recipe.library.updated` | public | `cynthus-audit` |
| `public.recipe.library.deleted` | public | `cynthus-audit` |
| `audit.recipe.library.role_assigned` | audit | `cynthus-audit` |
| `audit.recipe.library.role_revoked` | audit | `cynthus-audit` |
| `public.recipe.created` | public | `cynthus-core-api`, `cynthus-analysis`, `cynthus-audit` |
| `public.recipe.updated` | public | `cynthus-core-api`, `cynthus-analysis`, `cynthus-audit` |
| `public.recipe.deleted` | public | `cynthus-core-api`, `cynthus-audit` |
| `internal.recipe.import.url_submitted` | internal | `cynthus-worker` |
| `public.recipe.scaled` | public | `cynthus-core-api`, `cynthus-analysis`, `cynthus-audit` |
| `internal.recipe.pricing.updated` | internal | `cynthus-core-api` |
| `internal.recipe.ocr.image_submitted` | internal | `cynthus-worker` |
| `internal.recipe.scrape.url_submitted` | internal | `cynthus-worker` |
| `public.recipe.variant.saved` | public | `cynthus-core-api`, `cynthus-audit` |
| `internal.worker.job.queued` | internal | `cynthus-worker` |

**Consumes (8 signals)**

| Signal | Publisher |
|---|---|
| `public.meal.recipes.associated` | `cynthus-core-api` |
| `internal.recipe.import.completed` | `cynthus-worker` |
| `internal.recipe.import.failed` | `cynthus-worker` |
| `internal.recipe.modification.clinically_suggested` | `cynthus-chat` |
| `internal.recipe.ocr.completed` | `cynthus-worker` |
| `internal.recipe.scrape.completed` | `cynthus-worker` |
| `internal.recipe.nutrition.enriched` | `cynthus-worker` |
| `public.recipe.substitution.suggested` | `cynthus-chat` |

### `cynthus-logistics`

Inventory logistics (movement between locations, ordering, delivery).

No signals in the catalog.

### `cynthus-profile`

Preferences and hard constraints.

**Publishes (13 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `internal.profile.energy_level.updated` | internal | `cynthus-chat`, `cynthus-core-api` |
| `internal.profile.soft_preferences.updated` | internal | `cynthus-chat`, `cynthus-audit` |
| `audit.profile.hard_constraint.updated` | audit | `cynthus-audit` |
| `internal.profile.notification_preferences.updated` | internal | `cynthus-notification`, `cynthus-scheduler` |
| `internal.profile.favorite.added` | internal | `cynthus-chat`, `cynthus-analysis` |
| `internal.profile.favorite.removed` | internal | `cynthus-chat`, `cynthus-analysis` |
| `internal.profile.accessibility_preference.updated` | internal | `cynthus-chat`, `cynthus-core-api` |
| `internal.profile.locale.updated` | internal | `cynthus-core-api`, `cynthus-chat` |
| `public.profile.profile.responded` | public | `cynthus-core-api`, `cynthus-audit` |
| `public.profile.profile.created` | public | `cynthus-audit` |
| `public.profile.profile.updated` | public | `cynthus-audit` |
| `public.profile.profile.deleted` | public | `cynthus-audit` |
| `public.profile.snapshot.published` | public | `cynthus-analysis`, `cynthus-audit` |

**Consumes (3 signals)**

| Signal | Publisher |
|---|---|
| `public.engagement.attendee_joined` | `cynthus-core-api` |
| `public.profile.profile.requested` | `cynthus-core-api` |
| `audit.identity.user.authenticated` | `cynthus-identity` |

### `cynthus-shopping`

Shopping lists (named in the catalog and the code, not in ADD 6.0).

**Publishes (21 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `public.shopping_list.created` | public | `cynthus-audit` |
| `public.shopping_list.updated` | public | `cynthus-audit` |
| `public.shopping_list.deleted` | public | `cynthus-audit` |
| `public.shopping_list.item.added` | public | `cynthus-analysis`, `cynthus-audit` |
| `public.shopping_list.item.updated` | public | `cynthus-analysis`, `cynthus-audit` |
| `public.shopping_list.item.checked_off` | public | `cynthus-analysis`, `cynthus-audit` |
| `public.shopping_list.item.removed` | public | `cynthus-audit` |
| `audit.shopping_list.role_assigned` | audit | `cynthus-audit` |
| `audit.shopping_list.role_revoked` | audit | `cynthus-audit` |
| `internal.shopping_list.procurement_target.set` | internal | `cynthus-core-api`, `cynthus-scheduler` |
| `internal.shopping_list.item.vendor_preference_set` | internal | `cynthus-chat`, `cynthus-partner-api` |
| `audit.shopping_list.management_delegated` | audit | `cynthus-audit` |
| `audit.shopping_list.management_revoked` | audit | `cynthus-audit` |
| `public.shopping_list.access_requested` | public | `cynthus-notification`, `cynthus-audit` |
| `public.shopping_list.access_request_withdrawn` | public | `cynthus-notification`, `cynthus-audit` |
| `public.shopping_list.access_granted` | public | `cynthus-notification`, `cynthus-identity`, `cynthus-audit` |
| `public.shopping_list.access_denied` | public | `cynthus-notification`, `cynthus-audit` |
| `internal.shopping_list.autopurchase.schedule_configured` | internal | `cynthus-scheduler` |
| `public.shopping_list.autopurchase.confirmed` | public | `cynthus-partner-api`, `cynthus-billing-api`, `cynthus-audit` |
| `public.shopping_list.autopurchase.cancelled` | public | `cynthus-scheduler`, `cynthus-audit` |
| `public.shopping_list.autopurchase.modified` | public | `cynthus-scheduler`, `cynthus-audit` |

**Consumes (3 signals)**

| Signal | Publisher |
|---|---|
| `public.inventory.location.deleted` | `cynthus-inventory` |
| `public.inventory.item.low` | `cynthus-scheduler` |
| `internal.shopping_list.generation.completed` | `cynthus-chat` |

### `cynthus-scheduler`

Periodic time-based task management.

**Publishes (9 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `internal.meal.suggestion_schedule.triggered` | internal | `cynthus-core-api` |
| `public.inventory.item.low` | public | `cynthus-notification`, `cynthus-chat`, `cynthus-shopping`, `cynthus-audit` |
| `public.inventory.item.expiry_approaching` | public | `cynthus-notification`, `cynthus-chat`, `cynthus-analysis`, `cynthus-audit` |
| `public.inventory.item.expired` | public | `cynthus-notification`, `cynthus-chat`, `cynthus-audit` |
| `internal.inventory.item.prioritized_for_expiry` | internal | `cynthus-core-api` |
| `internal.shopping_list.autopurchase.reminder_due` | internal | `cynthus-notification`, `cynthus-chat` |
| `internal.shopping_list.meal_gap.detected` | internal | `cynthus-notification`, `cynthus-chat` |
| `public.promotion.expired` | public | `cynthus-notification`, `cynthus-partner-api`, `cynthus-audit` |
| `internal.account.deletion_confirmed` | internal | `cynthus-core-api`, `cynthus-worker`, `cynthus-audit` |

**Consumes (13 signals)**

| Signal | Publisher |
|---|---|
| `internal.meal.suggestion_schedule.configured` | `cynthus-core-api` |
| `public.meal.plan.created` | `cynthus-core-api` |
| `public.meal.plan.updated` | `cynthus-core-api` |
| `public.meal.plan.deleted` | `cynthus-core-api` |
| `public.inventory.item.added` | `cynthus-inventory` |
| `public.inventory.item.updated` | `cynthus-inventory` |
| `public.inventory.item.removed` | `cynthus-inventory` |
| `internal.shopping_list.procurement_target.set` | `cynthus-shopping` |
| `internal.shopping_list.autopurchase.schedule_configured` | `cynthus-shopping` |
| `public.shopping_list.autopurchase.cancelled` | `cynthus-shopping` |
| `public.shopping_list.autopurchase.modified` | `cynthus-shopping` |
| `internal.account.deletion_requested` | `cynthus-core-api` |
| `internal.profile.notification_preferences.updated` | `cynthus-profile` |

### `cynthus-worker`

Ingress and non-time-based task management.

**Publishes (11 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `internal.inventory.scan.completed` | internal | `cynthus-core-api` |
| `internal.recipe.import.completed` | internal | `cynthus-recipe` |
| `internal.recipe.import.failed` | internal | `cynthus-recipe`, `cynthus-notification` |
| `internal.recipe.ocr.completed` | internal | `cynthus-recipe` |
| `internal.recipe.scrape.completed` | internal | `cynthus-recipe` |
| `internal.recipe.nutrition.enriched` | internal | `cynthus-recipe` |
| `audit.account.data_erased` | audit | `cynthus-audit` |
| `internal.data_export.completed` | internal | `cynthus-notification` |
| `internal.worker.job.queued` | internal | `cynthus-worker` |
| `internal.worker.job.completed` | internal | - |
| `internal.worker.job.failed` | internal | `cynthus-notification` |

**Consumes (7 signals)**

| Signal | Publisher |
|---|---|
| `internal.inventory.scan.receipt_submitted` | `cynthus-core-api` |
| `internal.recipe.import.url_submitted` | `cynthus-recipe` |
| `internal.recipe.ocr.image_submitted` | `cynthus-recipe` |
| `internal.recipe.scrape.url_submitted` | `cynthus-recipe` |
| `internal.account.deletion_confirmed` | `cynthus-scheduler` |
| `internal.data_export.requested` | `cynthus-core-api` |
| `internal.worker.job.queued` | `cynthus-core-api`, `cynthus-recipe`, `cynthus-worker` |

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

| Signal | Topic | Consumers |
|---|---|---|
| `audit.identity.user.authenticated` | audit | `cynthus-audit`, `cynthus-profile` |
| `audit.identity.user.rejected` | audit | `cynthus-audit` |
| `audit.identity.token.issued` | audit | `cynthus-audit` |

**Consumes (13 signals)**

| Signal | Publisher |
|---|---|
| `public.shopping_list.access_granted` | `cynthus-shopping` |
| `public.group.created` | `cynthus-core-api` |
| `public.group.deleted` | `cynthus-core-api` |
| `public.group.member_added` | `cynthus-core-api` |
| `public.group.member_role_changed` | `cynthus-core-api` |
| `public.group.member_removed` | `cynthus-core-api` |
| `public.group.join_approved` | `cynthus-core-api` |
| `internal.system.subscription.upgraded` | `cynthus-billing-api` |
| `internal.system.subscription.downgraded` | `cynthus-billing-api` |
| `internal.system.entitlement.updated` | `cynthus-billing-api` |
| `audit.access.provider_data_consent_granted` | `cynthus-health-api` |
| `audit.access.provider_data_consent_revoked` | `cynthus-health-api` |
| `public.access.request.approved` | `cynthus-core-api` |

### `cynthus-audit`

Auditing and compliance.

**Publishes (1 signal)**

| Signal | Topic | Consumers |
|---|---|---|
| `audit.system.ledger.entry_written` | audit | - |

**Consumes (151 signals)**, by domain: AI Companion 3; Access Control 5; Account Management 15; Billing Management 3; Clinical Monitoring 5; Contribution Management 1; Engagement Management 6; Group Management 8; Inventory Management 29; Live Companion 2; Meal Planning 12; Messaging 4; Rating Management 2; Recipe Management 13; Security and Identity 11; Service and Resource Management 11; Shopping List 18; Tag Management 3.

### `cynthus-trust-cache`

Caching for trust services.

No signals in the catalog.

### `cynthus-trust-db`

Persistent storage for trust services.

No signals in the catalog.

## Cynthus Intelligence (closed source)

### `cynthus-chat`

Astri persona (conversational life assistant and companion).

**Publishes (9 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `public.meal.suggestion.generated` | public | `cynthus-core-api`, `cynthus-notification`, `cynthus-audit` |
| `public.meal.vote.auto_resolved` | public | `cynthus-core-api`, `cynthus-notification`, `cynthus-audit` |
| `internal.recipe.modification.clinically_suggested` | internal | `cynthus-recipe`, `cynthus-audit` |
| `public.recipe.substitution.suggested` | public | `cynthus-recipe`, `cynthus-audit` |
| `internal.shopping_list.generation.completed` | internal | `cynthus-shopping` |
| `internal.shopping_list.promotional_data.requested` | internal | `cynthus-partner-api` |
| `internal.live_session.step_advanced` | internal | `cynthus-messaging` |
| `internal.intelligence.chat.session_ended` | internal | `cynthus-core-api`, `cynthus-audit` |
| `internal.intelligence.chat.interaction_recorded` | internal | `cynthus-core-api`, `cynthus-audit` |

**Consumes (34 signals)**, by domain: AI Companion 2; Accessibility 4; Account Management 2; Clinical Monitoring 2; Engagement Management 3; Inventory Management 3; Meal Planning 6; Platform Infrastructure 2; Rating Management 3; Recipe Management 1; Service and Resource Management 2; Shopping List 4.

### `cynthus-analysis`

Sentiment, biometric trend, energy level and dietary trend analysis.

**Publishes (7 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `internal.meal.vote.stalemate_detected` | internal | `cynthus-chat` |
| `internal.health.telemetry.snapshot_recorded` | internal | `cynthus-audit` |
| `public.health.biometric.anomaly_detected` | public | `cynthus-notification`, `cynthus-chat`, `cynthus-health-api`, `cynthus-audit` |
| `internal.health.analysis.correlation_completed` | internal | `cynthus-chat`, `cynthus-health-api` |
| `internal.analysis.harmony_score.computed` | internal | `cynthus-core-api`, `cynthus-notification` |
| `internal.analytics.spend.snapshot_recorded` | internal | `cynthus-core-api` |
| `internal.analytics.trend.computed` | internal | `cynthus-partner-api` |

**Consumes (20 signals)**

| Signal | Publisher |
|---|---|
| `public.meal.suggestion.accepted` | `cynthus-core-api` |
| `public.meal.suggestion.denied` | `cynthus-core-api` |
| `public.meal.plan.created` | `cynthus-core-api` |
| `public.meal.plan.updated` | `cynthus-core-api` |
| `public.meal.plan.deleted` | `cynthus-core-api` |
| `public.meal.recipes.associated` | `cynthus-core-api` |
| `public.meal.vote.cast` | `cynthus-core-api` |
| `public.inventory.item.expiry_approaching` | `cynthus-scheduler` |
| `public.recipe.created` | `cynthus-recipe` |
| `public.recipe.updated` | `cynthus-recipe` |
| `public.recipe.scaled` | `cynthus-recipe` |
| `public.shopping_list.item.added` | `cynthus-shopping` |
| `public.shopping_list.item.updated` | `cynthus-shopping` |
| `public.shopping_list.item.checked_off` | `cynthus-shopping` |
| `public.rating.created` | `cynthus-core-api` |
| `public.rating.updated` | `cynthus-core-api` |
| `internal.profile.favorite.added` | `cynthus-profile` |
| `internal.profile.favorite.removed` | `cynthus-profile` |
| `internal.tag.assigned` | `cynthus-core-api` |
| `public.profile.snapshot.published` | `cynthus-profile` |

### `cynthus-video`

Heads-up display and real-time video for live and AI companion mode.

**Publishes (4 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `internal.spatial.object_detected` | internal | `cynthus-chat` |
| `internal.spatial.frame_processed` | internal | `cynthus-chat` |
| `internal.spatial.object_detected` | internal | `cynthus-chat` |
| `internal.spatial.frame_processed` | internal | `cynthus-chat` |

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

| Signal | Topic | Consumers |
|---|---|---|
| `audit.health.provider_data_access` | audit | `cynthus-audit` |
| `internal.health.rpm.transmission_logged` | internal | `cynthus-billing-api`, `cynthus-audit` |
| `internal.health.rpm.clinician_interaction_logged` | internal | `cynthus-billing-api`, `cynthus-audit` |
| `audit.access.provider_data_consent_granted` | audit | `cynthus-audit`, `cynthus-identity` |
| `audit.access.provider_data_consent_revoked` | audit | `cynthus-audit`, `cynthus-identity` |

**Consumes (2 signals)**

| Signal | Publisher |
|---|---|
| `public.health.biometric.anomaly_detected` | `cynthus-analysis` |
| `internal.health.analysis.correlation_completed` | `cynthus-analysis` |

### `cynthus-health-web`

UI renderer for clinical interactions.

No signals in the catalog.

### `cynthus-messaging`

Device telemetry hub.

**Publishes (4 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `public.messaging.message.sent` | public | `cynthus-notification`, `cynthus-audit` |
| `public.messaging.message.deleted` | public | `cynthus-audit` |
| `public.messaging.recipe.shared` | public | `cynthus-audit` |
| `public.messaging.inventory_item.shared` | public | `cynthus-audit` |

**Consumes (5 signals)**

| Signal | Publisher |
|---|---|
| `public.meal.vote.initiated` | `cynthus-core-api` |
| `public.meal.vote.cast` | `cynthus-core-api` |
| `public.group.deleted` | `cynthus-core-api` |
| `public.live_session.started` | `cynthus-core-api` |
| `internal.live_session.step_advanced` | `cynthus-chat` |

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

| Signal | Topic | Consumers |
|---|---|---|
| `internal.system.payment_method.updated` | internal | `cynthus-audit` |
| `internal.system.subscription.upgraded` | internal | `cynthus-identity`, `cynthus-audit` |
| `internal.system.subscription.downgraded` | internal | `cynthus-identity`, `cynthus-audit` |
| `internal.system.entitlement.updated` | internal | `cynthus-identity` |

**Consumes (5 signals)**

| Signal | Publisher |
|---|---|
| `public.inventory.order.initiated` | `cynthus-core-api` |
| `public.shopping_list.autopurchase.confirmed` | `cynthus-shopping` |
| `internal.health.rpm.transmission_logged` | `cynthus-health-api` |
| `internal.health.rpm.clinician_interaction_logged` | `cynthus-health-api` |
| `audit.partner.contribution_recorded` | `cynthus-partner-api` |

### `cynthus-partner-api`

Partner integrations.

**Publishes (11 signals)**

| Signal | Topic | Consumers |
|---|---|---|
| `public.inventory.order.submitted` | public | `cynthus-notification`, `cynthus-audit` |
| `public.inventory.order.failed` | public | `cynthus-notification`, `cynthus-audit` |
| `public.service_registry.created` | public | `cynthus-audit` |
| `public.service_registry.updated` | public | `cynthus-audit` |
| `public.service_registry.deleted` | public | `cynthus-audit` |
| `audit.service_registry.management_delegated` | audit | `cynthus-audit` |
| `public.promotion.created` | public | `cynthus-notification`, `cynthus-chat`, `cynthus-audit` |
| `public.promotion.updated` | public | `cynthus-notification`, `cynthus-audit` |
| `public.device_registry.device_listed` | public | `cynthus-audit` |
| `public.device_registry.device_removed` | public | `cynthus-audit` |
| `audit.partner.contribution_recorded` | audit | `cynthus-audit`, `cynthus-billing-api` |

**Consumes (9 signals)**

| Signal | Publisher |
|---|---|
| `public.inventory.order.initiated` | `cynthus-core-api` |
| `internal.shopping_list.item.vendor_preference_set` | `cynthus-shopping` |
| `internal.shopping_list.promotional_data.requested` | `cynthus-chat` |
| `public.shopping_list.autopurchase.confirmed` | `cynthus-shopping` |
| `public.promotion.expired` | `cynthus-scheduler` |
| `public.vendor.subscription_created` | `cynthus-core-api` |
| `public.vendor.subscription_removed` | `cynthus-core-api` |
| `internal.vendor_directory.search.performed` | `cynthus-core-api` |
| `internal.analytics.trend.computed` | `cynthus-analysis` |

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

| Signal | Topic | Consumers |
|---|---|---|
| `internal.identity.svid.issued` | internal | `cynthus-audit` |
| `internal.identity.svid.rotated` | internal | `cynthus-audit` |

### `spire-server`

Revokes SVIDs.

**Publishes (1 signal)**

| Signal | Topic | Consumers |
|---|---|---|
| `audit.identity.svid.revoked` | audit | `cynthus-audit` |

## Discrepancies found while generating this list

These are for the document owner to decide. Nothing here has been changed in the catalog or ADD 6.0.

1. **`cynthus-shopping` and `cynthus-notification`** are publishers or consumers in the catalog (21 and 41 signals) but are not in the ADD 6.0 service tables. `cynthus-shopping` also exists as a container in the `cynthus-core` repository.
2. **`cynthus-messaging`** is used in the catalog both for group-chat and interactive-card signals (ADD name: `cynthus-messaging-engine`) and as the device telemetry hub (ADD name: `cynthus-messaging`, in Health). One name, two services.
3. **`cynthus-inventory` and `cynthus-logistics`** are in ADD 6.0 but publish nothing in the catalog. Inventory signals are published by `cynthus-core-api` (13), `cynthus-scheduler` (4), `cynthus-partner-api` (2) and `cynthus-worker` (1). The older handling matrix had `cynthus-inventory` publishing the inventory topic.
4. **`cynthus-identity`** publishes nothing in the catalog (13 signals consumed). The older matrix had it publishing the Auth and System topics. The SVID signals are published by `spire-agent` and `spire-server`, which are not in ADD 6.0.
5. **Cache and database services, `cynthus-core-web`, `cynthus-health-web`** have no signals, as expected for stores and renderers.
