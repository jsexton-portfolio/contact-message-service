# Contact Message Service
![](https://github.com/jsexton-portfolio/contact-message-service/workflows/build/badge.svg)

Service used to interface with portfolio application contact messages

- [Endpoint Summary](#endpoint-summary)
- [Create Contact Message](#create-contact-message)
- [Retrieve Contact Messages](#retrieve-contact-messages)
- [Retrieve Contact Message](#retrieve-contact-message)

## Endpoint Summary
Base path: https://api.justinsexton.net/contact

- POST /mail
- GET /mail
- GET /mail/{id}

## Create Contact Message

Creates a new contact message resource

URL: `POST https://api.justinsexton.net/contact/mail`

### Request Body Schema
```json
{
  "message": "(Required: 100 minimum length - 2000 maximum length)",
  "reason": "(Required (Enum): Business|Question|Feedback|Other)",
  "sender": {
    "alias": "(Required: Sender's alias)",
    "phone": "(Optional: Sender's phone number)",
    "email": "(Required: Sender's email address)"
  } 
}
```

### Successful Response
```json
{
    "success": true,
    "meta": {
        "message": "string",
        "errorDetails": [],
        "paginationDetails": {},
        "schemas": {}
    },
    "data": {
        "contactMessageId": "string",
        "snsMessageId": "string"
    }
}
```

### Failed Response:
```json
{
    "success": false,
    "meta": {
        "message": "Given inputs were incorrect. Consult the below details to address the issue.",
        "errorDetails": [ 
          {
            "fieldName": "(The field name that caused an issue)",
            "description": "(Description detailing why the field caused an issue)"
          }
        ],
        "paginationDetails": {},
        "schemas": {
            "requestBody": {
                "title": "ContactMessageCreationForm",
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "maxLength": 2000,
                        "minLength": 100,
                        "type": "string"
                    },
                    "reason": {
                        "title": "Reason",
                        "enum": [
                            "business",
                            "question",
                            "feedback",
                            "other"
                        ]
                    },
                    "sender": {
                        "$ref": "#/definitions/SenderCreationForm"
                    }
                },
                "required": [
                    "message",
                    "reason",
                    "sender"
                ],
                "additionalProperties": false,
                "definitions": {
                    "SenderCreationForm": {
                        "title": "SenderCreationForm",
                        "type": "object",
                        "properties": {
                            "alias": {
                                "title": "Alias",
                                "type": "string"
                            },
                            "phone": {
                                "title": "Phone",
                                "type": "string"
                            },
                            "email": {
                                "title": "Email",
                                "type": "string",
                                "format": "email"
                            }
                        },
                        "required": [
                            "alias",
                            "email"
                        ],
                        "additionalProperties": false
                    }
                }
            }
        }
    },
    "data": null
}
```

## Retrieve Contact Messages

Retrieves list of contact messages

URL: `GET https://api.justinsexton.net/contact/mail`

Request Parameters:
- Archived: bool
- Reason: enum(business,question,feedback,other)
- Responded: bool
- Page: int
- Limit int

### Successful Response
```json
{
    "success": true,
    "meta": {
        "message": "Request completed successfully",
        "errorDetails": [],
        "paginationDetails": {},
        "schemas": {}
    },
    "data": {
        "count": 1,
        "contactMessages": [
            {
                "id": "5efc16bba9786d36ff48ff18",
                "message": "message",
                "reason": "reason",
                "archived": false,
                "responded": false,
                "sender": {
                    "alias": "alias",
                    "phone": "phone",
                    "email": "email",
                    "ip": "ip",
                    "userAgent": "userAgent"
                },
                "readers": [],
                "timeCreated": "2020-06-19T01:36:58.248000",
                "timeUpdated": "2020-06-19T01:36:58.248000"
            }
        ]
    }
}
```


## Retrieve Contact Message

Retrieves a single contact message by a specified ID

URL: `GET https://api.justinsexton.net/contact/mail/{id}`

```json
{
    "success": true,
    "meta": {
        "message": "Request completed successfully",
        "errorDetails": [],
        "paginationDetails": {},
        "schemas": {}
    },
    "data": {
        "id": "5efc16bba9786d36ff48ff18",
        "message": "message",
        "reason": "reason",
        "archived": false,
        "responded": false,
        "sender": {
            "alias": "alias",
            "phone": "phone",
            "email": "email",
            "ip": "ip",
            "userAgent": "userAgent"
        },
        "readers": [],
        "timeCreated": "2020-06-19T01:36:58.248000",
        "timeUpdated": "2020-06-19T01:36:58.248000"
    }
}
```
