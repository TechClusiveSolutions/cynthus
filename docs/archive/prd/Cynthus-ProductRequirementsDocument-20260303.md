# ?? Master Product Requirements Document: Cynthus

Product Name: Cynthus

Parent Organization: Tech-Clusive Solutions

Document Version: 4.0 (March 2026)

Status: High-Fidelity Design Phase

Guiding Principle: Universal Design and Accessibility-First Architecture.

## 1. Executive Summary

Cynthus is a multimodal lifestyle companion designed for individuals, families, and businesses. It integrates food logistics, inventory management, and medical alert functionality. By utilizing a choreographed microservice architecture, Cynthus bridges the gap between daily kitchen management and professional healthcare monitoring through wearable integration and a dedicated medical provider portal.

## 2. Strategic Objectives and Value Propositions

Cynthus creates a unique "Platform Network Effect" by connecting three distinct user groups.

### 2.1 User Value (Individuals and Families)

* Provide 100% accessible autonomy for blind, deaf, and neurodivergent users.
* Reduce "Decision Fatigue" through AI-powered meal planning and the "Energy Banker" system.
* Ensure safety through "Hard-Constraint" allergy and medical logic.

### 2.2 Provider Value (Doctors and Dietitians)

* Automate Remote Patient Monitoring (RPM) data collection.
* Provide clinical decision support through pantry and biometric analysis.
* Enable billable medical services via 2026 CPT codes (99445, 99470, 99454).

### 2.3 Partner Value (Hardware and Retailers)

* Increase wearable device utility (e.g., Garmin) by converting fitness trackers into medical tools.
* Drive targeted replenishment revenue for grocers and wholesalers through API integration.

## 3. User Personas and Stories

Each persona highlights a specific interaction with the Cynthus ecosystem.

### 3.1 The Parent (Admin)

* Story: As a blind parent, I need to perform a "Budget Audit" using Cynthus’s voice interface to ensure our $200 weekly grocery spend is on track while managing my children's nutritional needs.

### 3.2 The Medical User

* Story: As a user with Type 2 Diabetes, I need Cynthus to monitor my continuous glucose monitor (CGM) and cross-reference my pantry to suggest low-glycemic snacks when my levels are trending high.

### 3.3 The Small Business Owner (Caterer)

* Story: As an event planner, I need Cynthus to scale a recipe for 50 people with varying allergies and automatically generate a wholesale order for my partner grocer.

## 4. Functional Requirements and Hierarchy

Features are categorized by priority level (P1-P4). Priority 1 and 2 features are included in the Free Tier.

### 4.1 Priority 1: Operability and Accessibility (Free Tier)

* Cynthus-AI "Daily Spark": Contextual meal suggestions based on time of day.
* Allergy Hard-Filter: Absolute exclusion of unsafe ingredients from all suggestions.
* Sensory Profile: Real-time adaptation for screen readers (Blind), haptics/strobes (Deaf), and Zen Mode (Dyslexic).
* Basic Inventory: Standard logging of pantry, fridge, and freezer items.

### 4.2 Priority 2: Usability and Collaboration (Free Tier)

* Harmony Score: AI-mediated conflict resolution for group meal voting.
* Energy Banker: Filtering recipes based on current vs. future energy levels (Spoon Theory logic).
* Multimodal Wearable Integration: Basic sync with watches and rings for health statistics.
* Grocery Sync: Shared real-time lists for households and roommates.

### 4.3 Priority 3: Connectivity and Professional (Paid/Partner Tiers)

* Advanced Wearable HUD: Smart glasses support for step-by-step prep assistance.
* Preferential Replenishment: Automated ordering through partner grocer APIs.
* Advanced Costing: Real-time price-per-portion analysis for SMBs.

## 5. Medical and Clinical Specifications

This section outlines the requirements for the Cynthus-Portal and clinical integration.

### 5.1 Remote Patient Monitoring (RPM) Logic

* CPT 99445 Tracking: Automated logging of physiologic data transmission (2 to 15 days in a 30-day period).
* CPT 99470 Interaction: Logging of interactive communication time between clinical staff and patients.
* Clinical Dashboards: Triage-based views that flag patients with high-risk nutritional trends or biometric anomalies.

### 5.2 Symptom-Inventory Correlation

* AI-driven analysis linking inventory usage (e.g., high-sodium content) with reported symptoms (e.g., evening pain or heart rate spikes).

## 6. Technical Architecture

The system uses an Event-Driven Choreography pattern to ensure speed and modularity.

### 6.1 Service List

* SMH-Web: React/Next.js frontend optimized for SSR and accessibility.
* SMH-Auth: Multi-tenant authentication (RBAC + ABAC) with HIPAA audit logging.
* SMH-API: The "Choreographer" facilitating message routing via Redis.
* Cynthus-AI: The LLM Brain responsible for lifestyle logic and persona.
* SMH-Inventory: Predictive state manager for pantry and logistics.
* SMH-Scheduler: High-availability medical and nutritional triggers.
* SMH-Worker: Background processor for OCR, receipt scanning, and sync.
* SMH-Portal: The closed-source clinical gateway for healthcare providers.
* SMH-Cache/DB: Redis and PostgreSQL (Isolated schemas for clinical data).

## 7. Privacy and Compliance

As a medical-grade platform, Cynthus follows a "Privacy-Infrastructure" model.

### 7.1 Data Security

* Encryption: AES-256 for data at rest; TLS 1.3 for data in transit.
* PHI Isolation: Protected Health Information (PHI) is stored in a dedicated `vesta_clinical` database with field-level encryption.
* Audit Logs: Immutable logs of all data access, required for 2026 HIPAA Security Rule compliance.

### 7.2 Consent and Transparency

* Consent Bridge: Consensual sharing allows users to "invite" doctors into specific data streams.
* AI Transparency: Disclosure of AI use in any medical context, compliant with 2026 state-level AI governance laws (e.g., TRAIGA).

## 8. Business and Domain Strategy

Cynthus is launched under Tech-Clusive Solutions with a partner-centric revenue model.

### 8.1 Domain Portfolio

* Primary: `Cynthus.app` (Consumer Gateway).
* Defensive: `Cynthusmealhub.com` (Commercial Protection).
* Technical: `Cynthus.tech` (Developer and Consultancy Showcase).

### 8.2 Fee Schedule and Tiers

* Basic Tier (Individual/Family): Free. Includes P1 and P2 features.
* Plus Tier (Power User): $4.99/mo. Includes advanced wearable HUD and AI insights.
* Enterprise Tier (SMB/Caterer): $49.99/mo. Includes wholesale API and volume logistics.
* Provider Tier (Clinical): $99.00/mo. Includes Cynthus-Portal and RPM billing automation.

### 8.3 Revenue Drivers

* Partner "Bounties" for wearable device activations.
* Transaction fees on wholesale orders.
* Slotting fees for preferential replenishment placement by grocers.
* RPM revenue sharing with medical practices.
