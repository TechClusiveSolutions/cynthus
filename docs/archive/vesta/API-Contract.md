# Selda Ecosystem API Contract

Version: 1.0.0

## Overview

This is the contract between all of the services in the Selda ecosystem.

## Events

### Authentication

#### auth.login.requested

This event is emitted when a user requests an authentication token from the Auth Service.

##### Requestor

This request originates from the user's device

##### Data Collected

* User's IP address
* User's browser
* Request date and time

##### Request

POST /auth/token

``` JSON
{
    "email": "test.user@example.com",
    "password": "LetMeIn123*"
}
```

###### Parameters

* email: string
* password: string

##### Response

###### Success

``` JSON
{
    "data": {
        "token": "..."
    },
    "status": "success"
}
```

###### InvalidCredentialsError

``` JSON
{
    "error":{
        "message": "Login failed",
        "reason": "invalid_credentials"
    },
    "status": "failure"
}
```

## Messages

### requestAcknowledged

This message indicates that a request has been accepted and is being processed.

#### Sender

API Service

#### Recipient

User's device

#### Medium

Web socket

#### HTTP Status Code

200

#### Headers

* Content-Type: application/json

####Payload

``` JSON
{
    "status": "accepted"
}
```

### LoginRequest

## Errors
