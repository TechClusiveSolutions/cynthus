# Cynthus Life Ecosystem — Feature Registry

**Document Version:** 1.1 (June 2026)
**Status:** Final — all pricing, booster packs, base tier limits, and open items resolved
**Companion Document:** Cynthus PRD v4.1

---

## Document Notes

The following normalization actions were applied to the raw feature input:

- **Duplicates removed:** Features that appeared twice (once with empty fields, once complete) were consolidated into a single entry using the complete data.
- **Partial-data features completed:** Two inventory management features (`FT-IM-001`, `FT-IM-002`) existed only in the first block with partial fields. Descriptions and subscription tiers were inferred from the established pattern of adjacent inventory features.
- **Naming correction:** One reference to `Supplier-Basic` normalized to `Supplier-IM-Basic` for consistency with the tier naming convention.
- **All pricing finalized:** CM, DA, and Partner tier pricing established in v1.1. MI-Enterprise annual corrected to $500 (restoring ~17% annual discount). See Section 2.
- **Partner tier structure defined:** Partner tiers formally established as Community (Free), Integration ($199/month), and Strategic (Custom). See Section 2.7.
- **Base tier limits added:** Section 2.8 defines the default resource ceilings per tier that govern booster pack applicability.
- **Booster Pack Registry added:** Section 6 defines all available add-on packs with per-unit pricing across all account types.

---

## 1. Account Types

| Account Type | Definition | User-Facing Label |
|---|---|---|
| **Residential** | Individuals, families, teams, or informal associations using Cynthus for personal and household life-logistics. | User |
| **Commercial** | Businesses, organizations, or enterprises using Cynthus for professional food-service, catering, or operational logistics. | Manager / Organization |
| **Provider** | Professional entities that provide services to users within the ecosystem (e.g., clinicians, dietitians, health practices). | Provider |
| **Supplier** | Professional entities that supply physical goods to users or commercial accounts within the ecosystem (e.g., grocers, wholesalers, distributors). | Supplier |
| **Partner** | Professional entities that collaborate with, contribute to, or invest in the Cynthus platform (e.g., hardware manufacturers, strategic investors, open-source sponsors). | Partner |

---

## 2. Subscription Tier Matrix

### 2.1 Tier Naming Convention

Tiers follow the format: `{AccountType}-{Class}-{Level}`

- **Account Type:** `Residential`, `Commercial`, `Provider`, `Supplier`, `Partner`
- **Class:** `MP` (Meal Planning only), `IM` (Inventory Management only), `MI` (Meal Planning + Inventory Management), `CM` (Clinical Monitoring), `DA` (Data Analytics)
- **Level:** `Basic`, `Premium`, `Professional`, `Enterprise`

In the Feature Registry (Section 3), tiers are referenced using the shorthand `{Class}-{Level}` (e.g., `MP-Basic`). The applicable Account Types for each feature are listed in the "Available To" field, which together with the shorthand implies the full tier code.

### 2.2 Meal Planning Only (MP)

| Tier | Monthly | Annual | Annual Savings |
|---|---|---|---|
| Residential-MP-Basic | $0 | $0 | — |
| Residential-MP-Premium | $10 | $100 | ~17% (≈2 months free) |
| Residential-MP-Professional | $20 | $200 | ~17% |
| Residential-MP-Enterprise | $30 | $300 | ~17% |
| Commercial-MP-Basic | $0 | $0 | — |
| Commercial-MP-Premium | $10 | $100 | ~17% |
| Commercial-MP-Professional | $20 | $200 | ~17% |
| Commercial-MP-Enterprise | $30 | $300 | ~17% |

### 2.3 Inventory Management Only (IM)

| Tier | Monthly | Annual | Annual Savings |
|---|---|---|---|
| Residential-IM-Basic | $0 | $0 | — |
| Residential-IM-Premium | $10 | $100 | ~17% |
| Residential-IM-Professional | $20 | $200 | ~17% |
| Residential-IM-Enterprise | $30 | $300 | ~17% |
| Commercial-IM-Basic | $0 | $0 | — |
| Commercial-IM-Premium | $10 | $100 | ~17% |
| Commercial-IM-Professional | $20 | $200 | ~17% |
| Commercial-IM-Enterprise | $30 | $300 | ~17% |
| Supplier-IM-Basic | $0 | $0 | — |
| Supplier-IM-Premium | $10 | $100 | ~17% |
| Supplier-IM-Professional | $20 | $200 | ~17% |
| Supplier-IM-Enterprise | $30 | $300 | ~17% |

### 2.4 Meal Planning + Inventory Management (MI)

| Tier | Monthly | Annual | Annual Savings |
|---|---|---|---|
| Residential-MI-Basic | $0 | $0 | — |
| Residential-MI-Premium | $15 | $150 | ~17% |
| Residential-MI-Professional | $30 | $300 | ~17% |
| Residential-MI-Enterprise | $50 | $500 | ~17% |
| Commercial-MI-Basic | $0 | $0 | — |
| Commercial-MI-Premium | $15 | $150 | ~17% |
| Commercial-MI-Professional | $30 | $300 | ~17% |
| Commercial-MI-Enterprise | $50 | $500 | ~17% |

### 2.5 Clinical Monitoring (CM)

Basic tier is free forever with a 3-patient cap and view-only access, enabling solo practitioners to pilot the platform before committing. HIPAA-compliant infrastructure overhead is managed by keeping the free patient cap very low.

| Tier | Monthly | Annual | Annual Savings | Included Patients |
|---|---|---|---|---|
| Provider-CM-Basic | $0 | $0 | — | 3 (view-only) |
| Provider-CM-Premium | $149 | $1,490 | ~17% | 25 |
| Provider-CM-Professional | $299 | $2,990 | ~17% | 50 |

> Per-patient booster pricing above included thresholds: $8/patient/month (Premium), $6/patient/month (Professional). See Section 6.

### 2.6 Data Analytics (DA)

Analytics-only tiers for providers and suppliers who want reporting and insights without full clinical monitoring or inventory management features.

| Tier | Monthly | Annual | Annual Savings |
|---|---|---|---|
| Provider-DA-Basic | $0 | $0 | — |
| Provider-DA-Premium | $49 | $490 | ~17% |
| Provider-DA-Professional | $99 | $990 | ~17% |
| Supplier-DA-Basic | $0 | $0 | — |
| Supplier-DA-Premium | $29 | $290 | ~17% |
| Supplier-DA-Professional | $79 | $790 | ~17% |

### 2.7 Partner Tiers

Partner accounts are relationship-driven. Tiers reflect increasing platform integration depth rather than feature unlocks.

| Tier | Monthly | Annual | Annual Savings | Description |
|---|---|---|---|---|
| Partner-Community | $0 | $0 | — | Open-source access, developer documentation, community forums. No device registry or promotion listings. |
| Partner-Integration | $199 | $1,990 | ~17% | Device and system registry, promotion listings, basic device usage reporting, standard API access. |
| Partner-Strategic | Custom | Custom | Negotiated | Full platform integration rights, co-development collaboration, co-marketing, custom revenue-sharing, dedicated partner success contact. |

### 2.8 Base Tier Limits

Base tier limits define the default resource ceilings per subscription level. Booster packs (Section 6) allow users to expand any single dimension without upgrading their full tier.

#### Consumer (Residential & Commercial)

| Resource | Basic | Premium | Professional | Enterprise |
|---|---|---|---|---|
| Groups | 1 | 3 | 10 | Unlimited |
| Members per group | 5 | 15 | 50 | Unlimited |
| Inventory locations | 3 | 10 | 30 | Unlimited |
| Recipe libraries | 1 | 3 | 10 | Unlimited |
| Recipes per library | 100 | 500 | Unlimited | Unlimited |
| Data retention | 6 months | 2 years | 5 years | Unlimited |
| Astri chat | Unlimited | Unlimited | Unlimited | Unlimited |
| Astri advanced analytics | — | ✓ | ✓ | ✓ |
| Concurrent active engagements | — | 5 | 25 | Unlimited |

#### Supplier

| Resource | Supplier-IM-Basic | Supplier-IM-Premium | Supplier-IM-Professional | Supplier-IM-Enterprise |
|---|---|---|---|---|
| Inventory locations | 5 | 25 | 100 | Unlimited |
| Concurrent promotions | — | 3 | 10 | Unlimited |
| Data retention | 3 months | 1 year | 3 years | Unlimited |
| DA reports | — | Basic | Advanced | Full API |

#### Provider

| Resource | CM-Basic | CM-Premium | CM-Professional |
|---|---|---|---|
| Active patients | 3 | 25 | 50 |
| Dashboard access | View-only | Full | Full |
| RPM billing automation | — | ✓ | ✓ |
| Triage alerts | — | ✓ | ✓ |
| Multi-provider practice | — | — | ✓ |
| Additional practice locations | — | 1 | Unlimited |

#### Partner

| Resource | Community | Integration | Strategic |
|---|---|---|---|
| Device registry listings | — | 25 | Unlimited |
| Concurrent promotions | — | 5 | Unlimited |
| API access | Read-only docs | Standard | Full + dedicated support |

---

## 3. Feature Registry

Features are organized by functional domain. Each entry includes a stable feature ID for cross-referencing.

**Priority definitions:** `High` = foundational or safety-critical; `Medium` = significant value but not blocking; `Low` = enhancement or differentiator.

---

### Domain: Meal Planning

---

**FT-MP-001 — On-Demand AI Meal Suggestion**
> As a user, I want the ability to get an AI-generated meal suggestion upon request.

| Field | Value |
|---|---|
| Description | User-initiated request to Astri for a single contextual meal recommendation based on current inventory, time of day, and active preference/constraint profile. |
| Priority | High |
| Implementation Phase | 1 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-MP-002 — Scheduled Meal Suggestion Subscription**
> As a user, I want the ability to subscribe to AI-generated meal suggestions on a schedule: whenever I log in, daily, weekly, or monthly.

| Field | Value |
|---|---|
| Description | Configurable cadence for proactive Astri meal suggestions pushed to the user at login, or on a daily, weekly, or monthly schedule. |
| Priority | Medium |
| Implementation Phase | 1 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-MP-003 — Browse Meals by Category**
> As a user, I want the ability to select a meal from a list of available meals by category.

| Field | Value |
|---|---|
| Description | Manual browsing interface allowing users to explore meal options organized by food category (e.g., breakfast, lunch, dinner, snack, cuisine type). |
| Priority | High |
| Implementation Phase | 1 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-MP-004 — Create a Meal Plan**
> As a user, I want the ability to create a meal plan for a day, week, or month.

| Field | Value |
|---|---|
| Description | Planning canvas allowing users to schedule meals across a defined time horizon, with optional Astri-assisted population based on preferences and inventory state. |
| Priority | High |
| Implementation Phase | 1 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-MP-005 — Accept or Deny a Meal Suggestion**
> As a user, I want the ability to accept or deny a meal suggestion that I have received.

| Field | Value |
|---|---|
| Description | Binary response interface for Astri-generated suggestions. A denial triggers a follow-up suggestion. Responses are stored to inform future recommendation models. |
| Priority | High |
| Implementation Phase | 1 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-MP-006 — Associate a Meal with Multiple Recipes**
> As a user, I want the ability to associate a meal with multiple recipes.

| Field | Value |
|---|---|
| Description | Allows a single meal entry to reference multiple recipe components (e.g., a main dish and side dishes), enabling composite meal planning and accurate inventory consumption calculation. |
| Priority | Low |
| Implementation Phase | 3 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Premium, MI-Premium |

---

**FT-MP-007 — Propose a Group Meal and Initiate a Vote**
> As a user, I want the ability to propose a specific meal to a group I belong to and initiate a voting session.

| Field | Value |
|---|---|
| Description | Initiates a simple poll within a family or group unit where members can vote to build alignment on a meal choice. |
| Priority | High |
| Implementation Phase | 3 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-MP-008 — Cast a Vote on a Group Meal Proposal**
> As a user, I want the ability to cast a vote (Yes/No) on a meal proposed by another member of my group.

| Field | Value |
|---|---|
| Description | Real-time interactive poll interface allowing group members to submit their immediate meal preferences in response to an active proposal. |
| Priority | High |
| Implementation Phase | 3 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-MP-009 — View Real-Time Group Vote Results**
> As a user, I want the ability to view the real-time results and consensus percentage of an active group meal vote.

| Field | Value |
|---|---|
| Description | Visual breakdown showing who has voted and what the current group consensus is, calculated and updated automatically as votes are submitted. |
| Priority | Medium |
| Implementation Phase | 3 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-MP-010 — Astri Auto-Resolves a Split Vote**
> As a user, I want Astri to automatically resolve a split vote or stalemate based on historical group preferences and item expiry dates.

| Field | Value |
|---|---|
| Description | Premium analytical logic where Astri acts as an impartial tie-breaker when a group vote is split, optimizing for historical preference patterns and low food waste. |
| Priority | Medium |
| Implementation Phase | 4 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Premium, MI-Premium |

---

### Domain: Inventory Management

---

**FT-IM-001 — Create and Manage an Inventory Location**
> As a user, I want the ability to create and manage an inventory location for storing items.

| Field | Value |
|---|---|
| Description | Create named inventory containers representing physical storage spaces (e.g., pantry, fridge, freezer, warehouse section, cooler). Includes the ability to edit, archive, and delete locations the user owns. |
| Priority | High |
| Implementation Phase | 2 |
| Available To | Residential, Commercial, Supplier |
| Subscription Tiers | IM-Basic, MI-Basic, Supplier-IM-Basic |

---

**FT-IM-002 — Assign Roles to an Inventory Location**
> As a user, I want the ability to assign administrators, managers, contributors, and viewers to an inventory location that I created or that I can manage.

| Field | Value |
|---|---|
| Description | Granular RBAC delegation for individual inventory locations. Supports four permission levels: Administrator (full control including deletion), Manager (configuration and item management), Contributor (add/edit items), and Viewer (read-only access). |
| Priority | High |
| Implementation Phase | 3 |
| Available To | Residential, Commercial, Supplier |
| Subscription Tiers | IM-Basic, MI-Basic, Supplier-IM-Basic |

---

**FT-IM-003 — Add Items to an Inventory Location**
> As a user, I want the ability to add items to an inventory location that I created or that I can manage.

| Field | Value |
|---|---|
| Description | Explicit manual entry, barcode scanning, or quick-add of physical items into an active inventory location. |
| Priority | High |
| Implementation Phase | 2 |
| Available To | Residential, Commercial, Supplier |
| Subscription Tiers | IM-Basic, MI-Basic, Supplier-IM-Basic |

---

**FT-IM-004 — Subscribe to Inventory Location Notifications**
> As a user, I want the ability to subscribe to notifications for an inventory location that I have created or that I can access.

| Field | Value |
|---|---|
| Description | Configure real-time push, email, or webhook alerts for system state updates within a specific inventory location the user owns or has been granted access to. |
| Priority | Medium |
| Implementation Phase | 3 |
| Available To | Residential, Commercial, Supplier |
| Subscription Tiers | IM-Basic, MI-Basic, Supplier-IM-Basic |

---

**FT-IM-005 — Inventory Low Alert (Own Items)**
> As a user, I want the ability to get inventory low notifications for items that I have added to an inventory location.

| Field | Value |
|---|---|
| Description | Astri alerts the user when an item they added drops below a user-defined minimum threshold. |
| Priority | High |
| Implementation Phase | 2 |
| Available To | Residential, Commercial |
| Subscription Tiers | IM-Basic, MI-Basic |

---

**FT-IM-006 — Inventory Low Alert (Subscribed Location)**
> As a user, I want the ability to get inventory low notifications for items that are in an inventory location to which I have subscribed.

| Field | Value |
|---|---|
| Description | Shared notification stream allowing multiple family members, team managers, or location subscribers to receive alerts when group supplies drop below threshold. |
| Priority | Medium |
| Implementation Phase | 3 |
| Available To | Residential, Commercial, Supplier |
| Subscription Tiers | IM-Basic, MI-Basic, Supplier-IM-Premium |

---

**FT-IM-007 — Item Expiry Alert (Own Items)**
> As a user, I want the ability to get item expiry notifications for items that I have added to an inventory location.

| Field | Value |
|---|---|
| Description | Proactive alerting based on registered expiration dates to mitigate food waste and optimize cost-savings. |
| Priority | High |
| Implementation Phase | 2 |
| Available To | Residential, Commercial |
| Subscription Tiers | IM-Basic, MI-Basic |

---

**FT-IM-008 — Item Expiry Alert (Subscribed Location)**
> As a user, I want the ability to get item expiry notifications for items located in an inventory location to which I have subscribed.

| Field | Value |
|---|---|
| Description | Collaborative tracking of expiration states across a shared group, household, or commercial kitchen for all subscribed members. |
| Priority | Medium |
| Implementation Phase | 3 |
| Available To | Residential, Commercial, Supplier |
| Subscription Tiers | IM-Basic, MI-Basic, Supplier-IM-Premium |

---

**FT-IM-009 — Order Inventory Items from Service Providers**
> As a user, I want the ability to order new inventory items from service providers through the mobile app and the web portal.

| Field | Value |
|---|---|
| Description | One-click reordering or external cart synchronization (e.g., Instacart, Amazon Fresh) driven by low inventory levels. Free for consumers; transaction fee charged to the Supplier. |
| Priority | High |
| Implementation Phase | 5 |
| Available To | Residential, Commercial |
| Subscription Tiers | IM-Basic, MI-Basic |

---

### Domain: Recipe Management

---

**FT-RM-001 — Create a Recipe Library and Assign Roles**
> As a user, I want the ability to create a library of recipes and assign administrators, managers, contributors, and viewers.

| Field | Value |
|---|---|
| Description | Create isolated recipe repositories with granular RBAC for family units, professional kitchens, or public sharing. Supports Administrator, Manager, Contributor, and Viewer permission levels. |
| Priority | High |
| Implementation Phase | 2 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-RM-002 — Add Recipes to a Library**
> As a user, I want the ability to add recipes to a library that I have created or to which I can contribute.

| Field | Value |
|---|---|
| Description | Standard recipe input including structured metadata: ingredients, preparation steps, cook time, difficulty level, cost estimate, and tags. |
| Priority | High |
| Implementation Phase | 2 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-RM-003 — Search Recipes**
> As a user, I want the ability to search for recipes by keyword, title, ingredients, cook time, total cost, or difficulty level in libraries I have created or that I can access.

| Field | Value |
|---|---|
| Description | Multi-faceted lookup engine parsing recipe libraries to optimize meal choice based on immediate constraints. Results are always filtered against the user's active hard-constraint profile before being returned. |
| Priority | High |
| Implementation Phase | 2 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-RM-004 — Import Recipes from External Sources**
> As a user, I want the ability to import recipes from external resources and choose to which library they are added.

| Field | Value |
|---|---|
| Description | Web-scraping and parsing engine to ingest URL-based recipes, cleanly extracting structured ingredients and steps into the Cynthus recipe format. |
| Priority | Medium |
| Implementation Phase | 4 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Premium, MI-Premium |

---

**FT-RM-005 — AI Recipe Modification Suggestions**
> As a user, I want the ability to get recipe modification suggestions based on my medical profile and/or food preferences.

| Field | Value |
|---|---|
| Description | Astri processes closed-source health and telemetry data to suggest targeted ingredient swaps (e.g., reducing sodium for hypertension, replacing dairy for intolerance). Requires active Clinical Bridge consent. |
| Priority | High |
| Implementation Phase | 7 |
| Available To | Residential |
| Subscription Tiers | MP-Professional, MI-Professional |

---

### Domain: Group Management

---

**FT-GM-001 — Create and Manage a Group**
> As a user, I want the ability to create and manage a group of users: family, friend group, team, association, organization, or company.

| Field | Value |
|---|---|
| Description | Define organizational unit boundaries for resource, data, and workspace isolation. Groups are the primary multi-user tenancy container for Phase 2 and beyond. |
| Priority | High |
| Implementation Phase | 1 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers (Basic) |

---

**FT-GM-002 — Add Users to a Group and Assign Roles**
> As a user, I want the ability to add other users to a group that I have created or that I manage and assign those users a role in the group: member, manager, or viewer.

| Field | Value |
|---|---|
| Description | Core RBAC implementation for multi-user workspace tenancy. Supports three group-level roles: Member (standard access), Manager (configuration and delegation rights), and Viewer (read-only). |
| Priority | High |
| Implementation Phase | 1 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers (Basic) |

---

**FT-GM-003 — Join a Group**
> As a user, I want the ability to join a group that another user has created.

| Field | Value |
|---|---|
| Description | Invitation and validation loop allowing users to securely link their profiles to an external group tenancy via invite code or direct invitation from a group manager. |
| Priority | High |
| Implementation Phase | 1 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers (Basic) |

---

### Domain: Engagement Management

---

**FT-EM-001 — Create and Manage an Engagement**
> As a user, I want the ability to create and manage an engagement including: location, attendees (with food preferences), venue, materials needed, logistical considerations, and time period.

| Field | Value |
|---|---|
| Description | Advanced event coordinator that cross-references attendee preference matrices and hard-constraint profiles with inventory and logistics data to assist with planning a real-world gathering. |
| Priority | Medium |
| Implementation Phase | 4 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Premium, MI-Premium, Commercial-MP-Basic |

---

**FT-EM-002 — Join an Engagement**
> As a user, I want the ability to join an engagement that another user has created.

| Field | Value |
|---|---|
| Description | RSVP workflow that shares the joining user's dietary preferences and hard constraints with the engagement host automatically upon acceptance. |
| Priority | Medium |
| Implementation Phase | 4 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

**FT-EM-003 — Assign an Engagement Manager**
> As a user, I want the ability to assign another user as a manager of an engagement that I created or that I can manage.

| Field | Value |
|---|---|
| Description | Delegation of engagement configuration permissions to co-hosts or professional event planners within the workspace. |
| Priority | Low |
| Implementation Phase | 4 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Premium, MI-Premium, Commercial-MP-Basic |

---

### Domain: Live Companion

---

**FT-LC-001 — Live Peer and Provider Assistance**
> As a user, I want the ability to engage with other users and service providers through the mobile app or web portal to get live assistance while preparing and/or managing meals, inventory, or engagements.

| Field | Value |
|---|---|
| Description | Real-time peer-to-peer and client-to-vendor communication channels (text chat and voice) built directly into workspace contexts, enabling live cooking assistance or vendor consultation without leaving the app. |
| Priority | Low |
| Implementation Phase | 6 |
| Available To | Residential, Commercial, Supplier |
| Subscription Tiers | MP-Professional, MI-Professional, Supplier-IM-Premium |

---

### Domain: AI Companion

---

**FT-AI-001 — Astri AI Companion**
> As a user, I want the ability to engage with an AI agent through the mobile app or web portal to get live assistance while preparing and/or managing meals, inventory, or engagements.

| Field | Value |
|---|---|
| Description | Deep integration of Astri, the Cynthus AI persona, pulling pre-assembled context from inventory, recipe, and profile states to act as a conversational lifestyle assistant across all core domains. |
| Priority | High |
| Implementation Phase | 1 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, MI-Basic |

---

### Domain: Messaging

---

**FT-MS-001 — Group Real-Time Text Messaging**
> As a user, I want the ability to send and receive real-time text messages within an isolated chat channel dedicated to my group.

| Field | Value |
|---|---|
| Description | Core intra-group communication fabric for discussing meal options, coordination, and household or organizational logistics. Each group has one or more isolated chat channels. |
| Priority | High |
| Implementation Phase | 3 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers (Basic) |

---

**FT-MS-002 — Interactive In-Chat Cards**
> As a user, I want meal suggestions, voting cards, and low-inventory alerts to render interactively directly inside our group chat stream.

| Field | Value |
|---|---|
| Description | In-line rich text and interactive components within the chat view, allowing users to vote on a meal, acknowledge an alert, or view a suggestion without leaving the conversation thread. |
| Priority | High |
| Implementation Phase | 3 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers (Basic) |

---

**FT-MS-003 — Share Recipe or Inventory Item to Chat**
> As a user, I want the ability to share a specific recipe or inventory item directly into a chat channel.

| Field | Value |
|---|---|
| Description | One-click sharing from the recipe library or pantry inventory view directly into an active group chat thread as a rich link card. |
| Priority | Medium |
| Implementation Phase | 3 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, IM-Basic, MI-Basic |

---

### Domain: Clinical Monitoring

---

**FT-CL-001 — Stream Wearable Telemetry**
> As a user, I want the ability to stream wearable telemetry to the app for real-time biometric analysis and medical alerting.

| Field | Value |
|---|---|
| Description | High-frequency data ingestion engine interfacing with health platform APIs (Apple HealthKit, Android Health Connect) to pipe biometric telemetry into Astri's analytical engine for real-time trend analysis and threshold alerting. |
| Priority | High |
| Implementation Phase | 7 |
| Available To | Residential |
| Subscription Tiers | MI-Professional, MI-Enterprise |

---

**FT-CL-002 — Provider Access to User Health Data**
> As a service provider, I want the ability to access a user's meal, inventory, and biometric data.

| Field | Value |
|---|---|
| Description | Secure, auditable workspace for clinicians and dietitians to track patient dietary adherence and physiological metrics. Access is gated by user consent (see FT-AC-001) and all access events are immutably logged. |
| Priority | High |
| Implementation Phase | 7 |
| Available To | Provider |
| Subscription Tiers | Provider-CM-Basic, Provider-CM-Premium |

---

### Domain: Service and Resource Management

---

**FT-SR-001 — Create and Manage a Service Registry**
> As a service provider, I want the ability to create and manage registries of services that I provide.

| Field | Value |
|---|---|
| Description | B2B interface allowing local suppliers, professional chefs, or health professionals to list their service capabilities, pricing, availability, and coverage areas within the Cynthus ecosystem. |
| Priority | High |
| Implementation Phase | 5 |
| Available To | Supplier, Provider |
| Subscription Tiers | Supplier-IM-Basic, Provider-CM-Basic |

---

**FT-SR-002 — Delegate Service Registry Management**
> As a service provider, I want the ability to designate others to manage my service registries.

| Field | Value |
|---|---|
| Description | Multi-user workspace provisioning for commercial vendor accounts, allowing staff or co-owners to manage service listings without sharing primary account credentials. |
| Priority | Medium |
| Implementation Phase | 5 |
| Available To | Supplier, Provider |
| Subscription Tiers | Supplier-IM-Premium, Provider-CM-Premium |

---

**FT-SR-003 — Create and Manage Service Promotions**
> As a service provider, I want the ability to create and manage a registry of service promotions.

| Field | Value |
|---|---|
| Description | Ad and discount injection engine letting suppliers offer targeted incentives to users based on real-time consumer shortage signals and inventory depletion patterns. |
| Priority | High |
| Implementation Phase | 5 |
| Available To | Supplier |
| Subscription Tiers | Supplier-IM-Premium |

---

**FT-SR-004 — Create and Manage a Device and System Registry**
> As a partner, I want the ability to create and manage a registry of devices and systems that I produce or sell.

| Field | Value |
|---|---|
| Description | Registry for hardware integrations including smart fridges, medical-grade wearables, IoT scales, and smart glasses. Partners register compatible devices for discovery and activation by end users. |
| Priority | Medium |
| Implementation Phase | 6 |
| Available To | Partner |
| Subscription Tiers | Partner-Integration, Partner-Strategic |

---

**FT-SR-005 — Create and Manage Device and Service Promotions**
> As a partner, I want the ability to create and manage a registry of device and service promotions that users can access.

| Field | Value |
|---|---|
| Description | Marketplace listings for hardware partnerships targeting highly relevant user segments based on profile, health tier, or inventory patterns. |
| Priority | Low |
| Implementation Phase | 6 |
| Available To | Partner |
| Subscription Tiers | Partner-Integration, Partner-Strategic |

---

### Domain: Contribution Management

---

**FT-CO-001 — Contribute to the Platform**
> As a partner, I want the ability to contribute money, devices, and systems to the project.

| Field | Value |
|---|---|
| Description | Portal to manage strategic investments, grants, hardware seed kits, or open-source sponsorships. Contributions are tracked and reportable (see FT-RP-004). |
| Priority | Low |
| Implementation Phase | 4 |
| Available To | Partner |
| Subscription Tiers | Partner-Community, Partner-Integration, Partner-Strategic |

---

### Domain: Billing Management

---

**FT-BL-001 — User Self-Service Billing Management**
> As a user, I want the ability to manage my billing information in the app or in a web portal.

| Field | Value |
|---|---|
| Description | Integration with payment processors (e.g., Stripe) for a self-service billing portal handling subscription upgrades, downgrades, payment method management, and billing history. |
| Priority | High |
| Implementation Phase | 3 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers |

---

**FT-BL-002 — Business Billing Portal**
> As a service provider, I want the ability to access and manage my billing information via a web portal.

| Field | Value |
|---|---|
| Description | Enterprise billing portal handling higher transaction limits, invoicing, corporate payout processing, and usage-based billing for B2B accounts. |
| Priority | High |
| Implementation Phase | 5 |
| Available To | Commercial, Supplier, Provider, Partner |
| Subscription Tiers | All Business Tiers |

---

### Domain: Account Management

---

**FT-AM-001 — Manage Contact Information**
> As a user, I want the ability to manage my contact information in the mobile app or in the web portal.

| Field | Value |
|---|---|
| Description | Standard user profile data management including name, email, phone number, and communication preferences. |
| Priority | High |
| Implementation Phase | 1 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers |

---

**FT-AM-002 — Manage Food Preferences and Medical Profile**
> As a user, I want the ability to manage my food preferences, medical information, venue preferences, and service provider preferences in the mobile app and in the web portal.

| Field | Value |
|---|---|
| Description | Core data matrix that defines the boundaries of Astri's analytical logic engine. Includes both soft preferences (favorite cuisines, portion sizes) and hard constraints (allergens, diagnosed conditions). See cynthus-profile service specification. |
| Priority | High |
| Implementation Phase | 2 |
| Available To | Residential, Commercial |
| Subscription Tiers | All Tiers |

---

**FT-AM-003 — Manage Subscription Preferences**
> As a user, I want the ability to manage my subscription preferences in the mobile app and in the web portal.

| Field | Value |
|---|---|
| Description | Tier-shifting and add-on selection interface. Handles upgrades, downgrades, and feature add-on management. |
| Priority | High |
| Implementation Phase | 3 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers |

---

**FT-AM-004 — Business Contact Profile Management**
> As a service provider, I want the ability to access and manage my contact information via a web portal.

| Field | Value |
|---|---|
| Description | Corporate profile management interface for commercial, supplier, and provider accounts. Includes organizational contact details, operational regions, and public-facing service descriptions. |
| Priority | High |
| Implementation Phase | 5 |
| Available To | Commercial, Supplier, Provider |
| Subscription Tiers | All Business Tiers |

---

**FT-AM-005 — Partner Account Management Portal**
> As a partner, I want the ability to manage my partner account via a web portal.

| Field | Value |
|---|---|
| Description | Dedicated dashboard for alliance-tier stakeholders to manage contributions, device registries, promotions, and reporting. |
| Priority | Medium |
| Implementation Phase | 6 |
| Available To | Partner |
| Subscription Tiers | Partner-Integration, Partner-Strategic |

---

**FT-AM-006 — Partner Contact Information Management**
> As a partner, I want the ability to access and manage my contact information via a web portal.

| Field | Value |
|---|---|
| Description | Standard operational record upkeep for partner organizations, including legal entity name, billing address, and primary contact details. |
| Priority | Medium |
| Implementation Phase | 6 |
| Available To | Partner |
| Subscription Tiers | Partner-Integration, Partner-Strategic |

---

**FT-AM-007 — Designate a Partner Account Contact**
> As a partner, I want the ability to designate a specific person as an account contact via a web portal.

| Field | Value |
|---|---|
| Description | Point-of-contact mapping for enterprise-level communication, allowing a partner organization to specify a named individual as the primary liaison for platform interactions. |
| Priority | Low |
| Implementation Phase | 6 |
| Available To | Partner |
| Subscription Tiers | Partner-Integration, Partner-Strategic |

---

### Domain: Rating Management

---

**FT-RT-001 — Rate Items, Meals, Recipes, Venues, and Providers**
> As a user, I want the ability to create and manage ratings for an item, meal, recipe, venue, or service provider.

| Field | Value |
|---|---|
| Description | Feedback loops used to optimize personal recommendation models and contribute to a global ecosystem reputation score. Ratings inform Astri's future suggestion ranking. |
| Priority | Medium |
| Implementation Phase | 4 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, IM-Basic, MI-Basic |

---

**FT-RT-002 — Manage Favorite Statuses**
> As a user, I want the ability to create and manage favorite statuses for an item, meal, recipe, inventory location, library, venue, or service provider.

| Field | Value |
|---|---|
| Description | Quick-access tagging enabling users to flag preferred entities for prioritized surfacing in Astri's suggestions and in browsing interfaces. |
| Priority | High |
| Implementation Phase | 2 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Basic, IM-Basic, MI-Basic |

---

### Domain: Tag Management

---

**FT-TG-001 — Create and Manage Custom Tags**
> As a user, I want the ability to create and manage tags that I can assign to an item, meal, recipe, inventory location, library, venue, or service provider.

| Field | Value |
|---|---|
| Description | Arbitrary user-defined taxonomy allowing deep structural personalization of custom data points beyond the system's built-in category schema. |
| Priority | Low |
| Implementation Phase | 4 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Premium, IM-Premium, MI-Premium |

---

### Domain: Access Control

---

**FT-AC-001 — Grant and Revoke Provider Data Access**
> As a user, I want the ability to grant and revoke permissions for service providers to access my meal, inventory, and biometric data (historical and real-time).

| Field | Value |
|---|---|
| Description | Privacy and security engine allowing fine-grained user data sovereignty over sensitive datasets. Users may scope access to specific data types and time windows, and may revoke at any time. All grant and revoke events are immutably logged. |
| Priority | High |
| Implementation Phase | 7 |
| Available To | Residential |
| Subscription Tiers | All Residential Tiers |

---

**FT-AC-002 — Accept or Deny Access Requests**
> As a user, I want the ability to accept or deny requests for access to inventory locations, libraries, groups, or engagements I have created or that I manage.

| Field | Value |
|---|---|
| Description | Inbound request authorization clearinghouse. Users receive structured access requests and can approve, deny, or defer them from within the app or web portal. |
| Priority | High |
| Implementation Phase | 1 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers |

---

**FT-AC-003 — Provider Requests Access to User Data**
> As a service provider, I want the ability to request access to a user's meal, inventory, and biometric data.

| Field | Value |
|---|---|
| Description | Structured outbound protocol for clinicians and suppliers to submit patient or consumer data authorization requests. Requests must specify the data scope and duration. |
| Priority | High |
| Implementation Phase | 7 |
| Available To | Provider, Supplier |
| Subscription Tiers | Provider-CM-Basic, Supplier-DA-Premium |

---

### Domain: Accessibility

---

**FT-AX-001 — Full Screen Reader Navigation**
> As a user, I want the ability to navigate all aspects of the mobile app and the web portal with a screen reader.

| Field | Value |
|---|---|
| Description | Implementation of rigorous semantic HTML, ARIA labels, and platform accessibility standards targeting WCAG 2.1 AA compliance. All Astri response payloads are structured for screen reader consumption without spatial or geometric layout dependencies. |
| Priority | High |
| Implementation Phase | 3 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers |

---

**FT-AX-002 — Visual and Haptic Notifications**
> As a user, I want the ability to get visual notifications and/or vibrations when my attention is needed in the mobile app.

| Field | Value |
|---|---|
| Description | Haptic feedback and explicit high-contrast visual indicators designed for inclusive accessibility, supporting users who are deaf or hard of hearing. |
| Priority | Medium |
| Implementation Phase | 3 |
| Available To | All Account Types |
| Subscription Tiers | All Tiers |

---

### Domain: Reporting and Compliance

---

**FT-RP-001 — User Data Access Report**
> As a user, I want the ability to access a report of service providers who have accessed my data over a period of time: daily, weekly, monthly, or yearly.

| Field | Value |
|---|---|
| Description | Compliance ledger report promoting total data transparency. Sourced from the immutable audit log maintained by `cynthus-audit`. |
| Priority | High |
| Implementation Phase | 8 |
| Available To | Residential |
| Subscription Tiers | All Residential Tiers |

---

**FT-RP-002 — Provider Service Usage Report**
> As a service provider, I want the ability to request a report of users who have used my services over a period of time: daily, weekly, monthly, quarterly, or yearly.

| Field | Value |
|---|---|
| Description | Basic business intelligence telemetry for operational vendors to track service engagement and optimize capacity planning. |
| Priority | High |
| Implementation Phase | 5 |
| Available To | Supplier, Provider |
| Subscription Tiers | Supplier-IM-Premium, Provider-CM-Premium |

---

**FT-RP-003 — Partner Device Usage Report**
> As a partner, I want the ability to request a report of usage data associated with the devices and systems that I provide.

| Field | Value |
|---|---|
| Description | High-level hardware usage statistics provided to engineering and manufacturing partners for product development and integration optimization. |
| Priority | Medium |
| Implementation Phase | 6 |
| Available To | Partner |
| Subscription Tiers | Partner-Integration, Partner-Strategic |

---

**FT-RP-004 — Partner Contribution Report**
> As a partner, I want the ability to request a report of my contributions to the project over a period of time: month, quarter, or year.

| Field | Value |
|---|---|
| Description | Accounting ledger for tracking capital expenditure, hardware grants, and open-source sponsorships toward the Cynthus ecosystem over a defined time period. |
| Priority | Low |
| Implementation Phase | 6 |
| Available To | Partner |
| Subscription Tiers | Partner-Integration, Partner-Strategic |

---

### Domain: Data Analytics and Dashboards

---

**FT-DA-001 — Group Sentiment and Satisfaction Dashboard**
> As a user, I want the ability to view a group dashboard that displays aggregated sentiment analysis results based on likes, dislikes, and recipe ratings.

| Field | Value |
|---|---|
| Description | Visual analytics dashboard summarizing household or group satisfaction trends, highlighting top crowd-pleasers and polarizing recipes based on accumulated rating and voting data. |
| Priority | Medium |
| Implementation Phase | 4 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Premium, MI-Premium, Commercial-MP-Premium |

---

**FT-DA-002 — Group Voting History and Consensus Dashboard**
> As a user, I want the ability to view a dashboard mapping group voting history to track consensus patterns and identify taste fatigue over time.

| Field | Value |
|---|---|
| Description | Visual reporting that highlights how quickly a group reaches consensus, which members are frequently out-voted, and when a household is hitting meal fatigue from repeating choices. |
| Priority | Low |
| Implementation Phase | 4 |
| Available To | Residential, Commercial |
| Subscription Tiers | MP-Premium, MI-Premium, Commercial-MP-Premium |

---

**FT-DA-003 — Enterprise Multi-Group Sentiment Dashboard**
> As a commercial manager, I want the ability to view multi-group sentiment and satisfaction trends across my entire corporate tenancy.

| Field | Value |
|---|---|
| Description | Enterprise-grade dashboard compiling sentiment and preference telemetry across multiple separate groups or sub-teams to drive broad logistical and purchasing decisions. |
| Priority | High |
| Implementation Phase | 8 |
| Available To | Commercial |
| Subscription Tiers | Commercial-MP-Enterprise, Commercial-MI-Enterprise |

---

## 4. Feature Summary by Phase

| Phase | Target | Feature IDs | Astri Version | Domain Focus |
|---|---|---|---|---|
| 1 | January 2027 | FT-MP-001–005, FT-AI-001, FT-AC-002, FT-AM-001 | Astri v1.0 | Core MVP: single-user accounts, on-demand meal suggestions, basic inventory, recipe library, AI companion (single-session, no cross-session memory) |
| 2 | Q2 2027 | FT-IM-001–003, FT-IM-005, FT-IM-007, FT-RM-001–003, FT-AM-002, FT-RT-002 | Astri v1.5 | Inventory intelligence, full profile management (soft prefs + hard constraints), recipe library, favorites. Astri gains profile persistence and inventory-aware proactive suggestions. |
| 3 | Q4 2027 | FT-MP-006–009, FT-GM-001–003, FT-IM-002, FT-IM-004, FT-IM-006, FT-IM-008, FT-MS-001–003, FT-BL-001, FT-AM-003, FT-AX-001–002 | Astri v2.0 | Multi-user group workspaces, real-time messaging, group meal voting, billing, subscription management, accessibility. Astri becomes group-aware, understanding all member profiles simultaneously. |
| 4 | H1 2028 | FT-MP-010, FT-RM-004, FT-EM-001–003, FT-CO-001, FT-RT-001, FT-TG-001, FT-DA-001–002 | Astri v2.5 | Engagement planning, recipe import, auto vote resolution, ratings, tags, analytics dashboards, partner contribution portal. Astri gains event-planning capability and early predictive meal fatigue detection. |
| 5 | H2 2028 | FT-IM-009, FT-SR-001–003, FT-BL-002, FT-AM-004, FT-RP-002 | Astri v3.0 | B2B commercial launch: supplier/provider service registries, inventory ordering, business billing, provider usage reports. Astri becomes commerce-aware, able to initiate reorders and scale recipes commercially. |
| 6 | H1 2029 | FT-LC-001, FT-SR-004–005, FT-AM-005–007, FT-RP-003–004 | Astri v3.5 | Live companion, partner platform, device/hardware registry, partner reporting. Astri provides real-time step-by-step cooking guidance and coordinates with live human companions. |
| 7 | H2 2029 | FT-CL-001–002, FT-RM-005, FT-AC-001, FT-AC-003 | Astri v4.0 | Clinical integration (pending regulatory approval): wearable telemetry, provider health data access, biometric recipe modifications, consent framework. Astri interprets biometric data and generates clinician-grade dietary guidance. |
| 8 | 2030 | FT-RP-001, FT-DA-003 | Astri v4.5 | Enterprise scale: compliance reporting, multi-tenancy sentiment analytics. Astri analyzes cross-organizational patterns and generates proactive enterprise-level recommendations. |

---

## 5. Open Items

All previously flagged open items are resolved as of v1.1. No outstanding items.

---

## 6. Booster Pack Registry

Booster packs allow users on any tier to expand a single resource dimension without a full tier upgrade. Packs are stackable (multiple packs of the same type may be purchased). Entitlements from active booster packs are reflected in the user's JWT claims via `cynthus-identity` and enforced at the ABAC layer — `cynthus-billing-api` owns the booster state and triggers a token refresh on every purchase or cancellation.

### 6.1 Residential Boosters

| Booster ID | Name | Unit | Price | Notes |
|---|---|---|---|---|
| BP-RES-001 | Group Size Pack | +5 members per group | $0.99/month | Stackable. Applies to one specified group per pack. |
| BP-RES-002 | Group Count Pack | +1 additional group | $0.99/month | Stackable. |
| BP-RES-003 | Library Pack | +1 recipe library | $0.99/month | Stackable. |
| BP-RES-004 | Location Pack | +1 inventory location | $1.99/month | Stackable. |
| BP-RES-005 | History Extension | +6 months data retention | $0.99/month | Stackable. Each pack extends retention window by 6 months. |

### 6.2 Commercial Boosters

Commercial packs provide larger unit increments at a higher per-pack price reflecting business-scale value. Per-member cost is lower per-unit than Residential when broken down, rewarding larger organizational needs.

| Booster ID | Name | Unit | Price | Notes |
|---|---|---|---|---|
| BP-COM-001 | Group Size Pack | +10 members per group | $4.99/month | Stackable. Applies to one specified group per pack. |
| BP-COM-002 | Group Count Pack | +1 additional group | $4.99/month | Stackable. |
| BP-COM-003 | Library Pack | +1 recipe library | $4.99/month | Stackable. |
| BP-COM-004 | Location Pack | +1 inventory location | $4.99/month | Stackable. |
| BP-COM-005 | History Extension | +1 year data retention | $9.99/month | Stackable. |
| BP-COM-006 | Engagement Slots | +5 concurrent active engagements | $9.99/month | Stackable. |

### 6.3 Provider Boosters

| Booster ID | Name | Unit | Price | Notes |
|---|---|---|---|---|
| BP-PRO-001 | Patient Capacity (Premium) | +1 patient/month above 25-patient threshold | $8.00/patient/month | Metered. Available on Provider-CM-Premium only. |
| BP-PRO-002 | Patient Capacity (Professional) | +1 patient/month above 50-patient threshold | $6.00/patient/month | Metered. Available on Provider-CM-Professional only. Rewards higher tier commitment. |
| BP-PRO-003 | Additional Practice Location | +1 physical practice location | $49.00/month | Stackable. |
| BP-PRO-004 | DA Add-on | Add Provider-DA-Premium analytics to a CM subscription | $29.00/month | Discounted vs. standalone DA-Premium ($49/month). |

### 6.4 Supplier Boosters

| Booster ID | Name | Unit | Price | Notes |
|---|---|---|---|---|
| BP-SUP-001 | Location Pack | +5 inventory locations | $9.99/month | Stackable. |
| BP-SUP-002 | Promotion Slots | +3 concurrent active promotions | $9.99/month | Stackable. |
| BP-SUP-003 | DA Add-on | Add Supplier-DA-Premium analytics to a Supplier-IM subscription | $19.00/month | Discounted vs. standalone DA-Premium ($29/month). |

### 6.5 Partner Boosters

| Booster ID | Name | Unit | Price | Notes |
|---|---|---|---|---|
| BP-PAR-001 | Device Registry Pack | +10 device/system listings | $49.00/month | Stackable. Available on Partner-Integration and above. |
| BP-PAR-002 | Promotion Pack | +5 concurrent partner promotions | $29.00/month | Stackable. Available on Partner-Integration and above. |

### 6.6 Architectural Note: Entitlement Enforcement

Booster pack purchases create a delta between a user's base tier entitlements and their effective entitlements. `cynthus-billing-api` is the single source of truth for active boosters. On every purchase or cancellation, `cynthus-billing-api` emits an `internal.system.entitlement.updated` signal on `cynthus-topic-internal`. `cynthus-identity` consumes this signal and issues a refreshed JWT reflecting the updated entitlement claims (e.g., `"max_group_members": 15` for a Basic user with two Group Size Packs active). Downstream services enforce limits using the token claims — they do not call `cynthus-billing-api` at runtime. This design is documented in ADR-005.
