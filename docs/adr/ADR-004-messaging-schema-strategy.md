# ADR 0004: Hybrid Open/Closed-Source Messaging Schema Strategy

## Status

Approved (June 2, 2026)

## Context

The Cynthus Life Ecosystem utilizes an asynchronous Choreographer Architecture distributed across open-source (`cynthus-core`, `cynthus-auth`) and closed-source (`cynthus-intelligence`) codebases.
Certain open-source infrastructure services (like `cynthus-api` and `cynthus-worker`) act as pass-through routers, processors, or consumers of signals originating from proprietary, closed-source domains (such as `lifestyle.harmony.calculated` and compliance `audit` tracking metrics).

Publishing 100% strict, static Pydantic schemas for these private domains within an open-source repository introduces:

1. Leakage of proprietary analytical intelligence vectors and algorithmic metadata.
2. Unnecessary exposure of internal system attack surfaces.
3. Release cycle blockages by coupling closed-source features to public repository updates.

## Decision

We will adopt a twin-strategy combining Layered Schema Distribution and Dynamic Envelope Ingestion:

1. Package Separation: The messaging contract codebase is split into two distinct repositories using Python implicit namespace packages under a unified top-level namespace:

   - `cynthus-messaging-public` (Open-Source / Public Wheel)
   - `cynthus-messaging-internal` (Closed-Source / Private Azure Artifact)

2. Opaque Payloads for Pass-Through Services: The global message envelope (`CynthusGlobalEnvelope`) in the public package will utilize a generic type variable with a fallback to a raw dictionary (`PayloadT = TypeVar("PayloadT", bound=Any, default=Any)`).
3. Validation Rules: Open-source pass-through services will parse and strictly validate only the outer envelope headers (such as `organization_id`, `workspace_id`, and `correlation_id`) to preserve multi-tenant security isolation. The inner `payload` will be treated as an un-inspected, read-only bucket of data (`dict`). Closed-source services will import the private package to apply deep, strongly-typed Pydantic model validation.

## Consequences

- Positive: Complete protection of closed-source intellectual property.
- Positive: Decoupled release management cycles for core vs. intelligence layers.
- Positive: Retains 100% strict type safety inside the dark subnets where processing happens.
- Negative: Pass-through services lose compile-time IDE auto-completion for the inner fields of private signals.
- Neutral: Local development setups must authenticate to the private Azure Artifacts feed to build intelligence services.
