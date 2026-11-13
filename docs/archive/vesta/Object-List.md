# ?? Selda Master Object List (Revised v3.0)

## 1. Identity & Access Domain (Auth Hub)

- **User**: Core identity. (ID, Email, PasswordHash, IsActive).
- **Organization**: A legal or logical entity (Family, Hospital, Grocer, Catering Co).
- *Properties*: `id`, `name`, `tax_id`, `parent_organization_id` (Self-referencing for Hospital/Office hierarchy).

- **Affiliation**: Maps a User to an Organization with a specific Role.
- *Properties*: `id`, `user_id`, `organization_id`, `role_id`, `permissions_json`.

---

## 2. Core Logistics & Measurement Domain (Core App)

- **Item**: The definition of a product (ID, Name, Barcode).
- **Shelf**: A storage container (ID, Organization_ID, Name, ShelfType).
- **InventoryItem**: The physical stock on a shelf (ID, Shelf_ID, Item_ID, Quantity, Expiry).
- **MeasurementSystem**: (ID, Name: e.g., 'Metric', 'Imperial').
- **MeasurementUnit**: (ID, Name, System_ID, Type_ID: e.g., 'Grams', 'Ounces').
- **MeasurementConversion**: Maps units to a **Standard Reference Unit**.
- *Properties*: `id`, `source_unit_id`, `target_unit_id`, `multiplier_to_standard`.
- *Logic*: All internal math is done in `Grams` or `Milliliters`. Use this only for UI display.

---

## 3. Culinary & Planning Domain (Core App)

- **Recipe**: The blueprint for a dish.
- **Ingredient**: Quantity of an Item required for a Recipe.
- **Instruction**: A specific Step in a Recipe.
- **Meal**: A specific instance of one or more Recipes being combined to be eaten.
- *Properties*: `id`, `name` (e.g., 'Tuesday Family Taco Night'), `total_calories`, `macro_summary_json`.

- **Schedule**: A temporal container for planning.
- *Properties*: `id`, `organization_id` (The Family or MSB), `start_date`, `end_date`.

- **Engagement (Scheduled Activity)**: A Meal or Task assigned to a time.
- *Properties*: `id`, `schedule_id`, `meal_id`, `activity_type` (Enum: 'Breakfast', 'Lunch', 'Prep'), `start_time`, `status` (Enum: 'Planned', 'Consumed', 'Skipped').

---

## 4. Clinical & Intelligence Domain (The Vault)

- **Signal**: The PubSub message (CorrelationID, Topic, Payload).
- **BiometricPulse**: Real-time health data (HeartRate, Glucose).
- **MedicalProfile**: Clinical status (IsDiabetic, BloodType).
- **Allergy**: Constraint mapping (User_ID, Item_ID, Severity).
- **RecommendationService**: Matches User data to Partner offerings.
- *Properties*: `id`, `service_type` (Enum: 'MealPrep', 'RPM', 'Replenishment'), `logic_version_id`, `input_signals_required`.

- **RecommendationResult**: The output of the AI.
- *Properties*: `id`, `user_id`, `recommendation_text`, `partner_offering_id`, `confidence_score`.

---

## 5. Commercial & Partner Domain (The Network)

- **Partner**: A Hardware, Software, or Retail collaborator (Garmin, Kroger).
- **Store**: A physical or digital retail location belonging to a Partner.
- *Properties*: `id`, `partner_id`, `location_id`, `api_endpoint_url`, `is_wholesaler` (Boolean).

- **PartnerOffering**: A product or service a Partner provides (e.g., 'Organic Oat Milk', 'RPM Dashboard').
- *Properties*: `id`, `partner_id`, `item_id` (if retail), `service_id` (if clinical), `price`, `discount_code_for_selda`.
