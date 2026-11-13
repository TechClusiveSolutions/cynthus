# Cynthus Life Signal Messages

## Open Source Schema

### Auth

Manages identity states, role/attribute changes, and cryptographic token handshakes.

#### auth.?.?

This signal is emitted bythe authentication engine when... It captures the following information:

*...

### Device

Manages aggregated warm-path time-slice telemetry blocks and instant real-time anomaly tracker boundary breaches.

#### device.battery.status

This signal is emitted by the Core API engine when a device sends a battery status update. It captures the following information:

- the device identifier
- the battery status data

#### device.biometric.trend

This signal is emitted by the  worker engine when a biometric trend has been calculated (every 15 minutes). It captures the following information:

- the user's identifier
- the device's identifier
- the metric type
- the time period start and end points
- the min value for the time period
- the max for the time period
- the average for the time period

### Inventory

Tracks mutations to space equipment logs, pantry supplies, and logistics asset states.

#### inventory.item.stock

This signal is emitted by the inventory engine when there is a change in the stock level of an item on a given pantry shelf. It captures the following information:

- the shelf owner's identifier
- the shelf identifier
- the pantry identifier
- the item identifier
- the stock level

### Logistics

Handles scaled recipe configurations and automated external B2B vendor inventory fulfillment routing.

### User

#### user.sentiment.record

This signal is emitted when a user takes an action that resulted in a sentiment data point (liked a meal, disliked a recipe, tagged a provider, etc). It captures the following information:

- the user identifier

- The action that was taken
- the entity that was acted upon
- action values (rating score, liked = true/false, etc)

#### user.energy.record

This signal is emitted when a user logs an energy level (too tired to cook, etc). It captures the following information:

- the user identifier
- energy level metric
- energy level consequence (need to find alternative meal option)

## Closed Source Schema

### Audit

Tracks B2B portal compliance intercepts and data inspections for HIPAA audit requirements.

#### audit.action.record

This signal is emitted when an action is taken by a user, a partner, or a provider. It captures the following information:

- the action that was taken (what)
- the entity that performed the action (who)
- which systems were impacted (where)
- when the action was performed (when)
- the reason the action was taken (why)

### Chat

Coordinates asynchronous conversational tracking, usage transparency metadata, and state auditing.

(Emits conversational metadata blocks, text layout linear summaries, and AI governance transparency logs)

#### chat.session.state

this signal is emitted by the chat engine when there is a change in the state of a chat session. It captures the following information:

- the user's identifier
- the chat's identifier
- the state of the chat session

#### chat.session.content

This signal is emitted by the chat engine when there is a dchange in the content of a chat session. It captures the following information:

- the user's identifier

- the chat's identifier
- the content of the chat session

### Lifestyle

Distributes computed 24-hour workspace harmony matrix scores, tracking tasks, variances, and operational indices.

#### lifestyle.harmony.calculation

This signal is emitted by the analysis engine when a harmony score calculation has been made. It captures the following information:

- harmony score
- score criteria
- group identifier

#### lifestyle.sentiment.analysis

this signal is emitted by the analysis engine when a pattern in a user's sentiment (meals, recipes, engagements, locations, etc) have been determined. it captures the following information:

- the user's identifier
- the sentiment identifier
- the results of the analysis

### System

Handles cross-cutting infrastructure state changes that force runtime behavior mutations across services, specifically the distribution of session parameters and ephemeral authorization keys.
