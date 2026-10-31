# Cynthus Events List

## Partner

### Partner.Promotion

#### Partner.Promotion.Created

A partner created a promotion

#### Partner.Promotion.Deleted

A partner deleted a promotion

## Provider

### Provider.Service

#### Provider.Service.Created

A provider created a service

#### Provider.Service.Deleted

A provider deleted a service

### Provider.ServiceList

#### Provider.ServiceList.Created

A provider created a service list

#### Provider.ServiceList.Deleted

A provider deleted a service list

#### Provider.ServiceList.ServiceAdded

A provider added a service to a service list

##### Payload

{
    "provider_id": "Provider1",
    "service_list_id": "ServiceList1",
    "offering_id": "Offering1"
}

####Provider.ServiceList.ServiceRemoved

A provider removed a service from a service list

### Provider.ServiceLocation

#### Provider.ServiceLocation.Created

a provider created a service location

## System

### System.Authentication

#### System.Authentication.SessionCreated

The authentication system created a session for a user

##### Payload

{
    "user_id": "User1"
}

#### System.Authentication.SessionExpired

The authentication system expired a session for a user

##### Payload

{
    "user_id": "User1"
}

### System.Inventory

#### System.Inventory.ItemExpirationNotificationCreated

The inventory system created an item expiration notification

##### Payload

{
    "inventory_id": "Inventory1",
    "shelf_id": "Shelf1",
    "item_id": "item1",
    "expires_on": "2026-06-01T00:00:00Z"
}

### System.Shutdown

#### system.shutdown.initiated

##### Payload

{
    "system_id": "System1",
    "reason": "maintenance"
}

### System.Startup

#### system.startup.initiated

The system has begun its startup process

##### Payload

{
    "system_id": "System1"
}

#### system.startup.completed

The system is available

##### Payload

{
    "system_id": "System1"
}

## User

### User.Group

#### User.Group.Created

A user created a group

##### Payload

{
    "user_id": "User1",
    "group_id": "Group1",
    "is_family": true,
    "is_primary": true,
    "created_on": "2026-06-01T08:00:00Z"
}

#### User.Group.Deleted

A user deleted a group

#### User.Group.MemberAdded

A user added a member to a group

##### Payload

{
    "user_id": "User1",
    "group_id": "Group1",
    "member_id": "User2"
}

#### User.Group.MemberRemoved

A user removed a member from a group

##### Payload

{
    "user_id": "User1",
    "group_id": "Group1",
    "member_id": "User2"
}

### User.Inventory

#### User.Inventory.Created

A user created an inventory

##### Payload

{
    "user_id": "User1",
    "inventory_id": "Inventory1",
    "created_on": "2026-06-01T08:00:00Z"
}

#### User.Inventory.Deleted

A user deleted an inventory

#### User.Inventory.ItemReplenished

A user replenished an item in an inventory

#### User.Inventory.ItemUsed

A user used an item from an inventory

#### User.Inventory.ShelfAdded

A user added a shelf to an inventory

##### Payload

{
    "user_id": "User1",
    "inventory_id": "Inventory1",
    "shelf_id": "Shelf1"
}

### User.Library

#### User.Library.Created

A user created a library

##### Payload

{
    "user_id": "User1",
    "library_id": "Library1",
    "created_on": "2026-06-01T08:00:00Z"
}

#### User.Library.Deleted

A user deleted a library

#### User.Library.RecipeAdded

A user added a recipe to a library

##### Payload

{
    "user_id": "User1",
    "library_id": "Library1",
    "recipe_id": "Recipe1"
}

### User.Meal

#### User.Meal.Created

A user created a meal

##### Payload

{
    "user_id": "User1",
    "meal_id": "Meal1",
    "created_on": "2026-06-01T08:00:00Z"
}

#### User.Meal.Deleted

A user deleted a meal

#### User.Meal.FavoriteAdded

The user added a favorite to a meal

##### Payload

{
    "user_id": "User1",
    "meal_id": "Meal1"
}

#### User.Meal.FavoriteRemoved

The user removed a favorite from a meal

##### Payload

{
    "user_id": "User1",
    "meal_id": "Meal1"
}

#### User.Meal.TagAdded

The user added a tag to a meal

##### Payload

{
    "user_id": "User1",
    "meal_id": "Meal1",
    "tag_id": "Tag1"
}

#### User.Meal.TagRemoved

The user removed a tag from a meal

##### Payload

{
    "user_id": "User1",
    "meal_id": "Meal1",
    "tag_id": "Tag1"
}

### User.Recipe

#### User.Recipe.Created

A user created a recipe

#### User.Recipe.Deleted

A user deleted a recipe

#### User.Recipe.Updated

A user updated a recipe

### User.Schedule

#### User.Schedule.Created

A user created a meal schedule

#### User.Schedule.MealAdded

A user added a meal to a meal Schedule

#### User.Schedule.MealRemoved

A user removed a meal from a meal schedule

#### User.Schedule.Updated

A user updated a meal schedule

### User.Shelf

#### User.Shelf.Craeated

A user created a shelf

##### Payload

{
    "user_id": "User1",
    "shelf_id": "Shelf1",
    "created_on": "2026-06-01T08:00:00Z"
}

#### User.Shelf.ItemAdded

A user added an item to a shelf

##### Payload

{
    "user_id": "User1",
    "shelf_id": "Shelf1",
    "item_id": "Item1",
    "expires_on": "2026-12-15T00:00:00Z"
}
