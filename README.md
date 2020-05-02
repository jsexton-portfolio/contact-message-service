# Contact Message Service
Service used to interface with portfolio application contact messages

## Endpoints

#### POST /mail

##### Request Body Schema:
```json
{
  "message": "(Required: 100 minimum length - 10000 maximum length)",
  "reason": "(Required (Enum): Business|Question|Feedback|Other)",
  "sender": {
    "alias": "(Required: Sender's alias)",
    "phone": "(Optional: Sender's phone number)",
    "email": "(Required: Sender's email address)"
  } 
}
```

##### Successful Response:
```json
{
    "success": true,
    "meta": {
        "message": "Request completed successfully",
        "errorDetails": [],
        "schemas": {}
    },
    "data": {
        "id": "5ead033114fc83a68c56eb9d",
        "message": "This is a test message that only needed to be longer than 100 characters long. Lets make this just a bit longer so that the database does not complain to us.",
        "reason": "question",
        "archived": false,
        "responded": false,
        "sender": {
            "alias": "Person",
            "phone": "1234567890",
            "email": "person@gmail.com",
            "ip": "127.0.0.1",
            "userAgent": "unknown"
        },
        "readers": [],
        "timeCreated": "2020-05-02T05:20:47.603908",
        "timeUpdated": "2020-05-02T05:20:47.603933"
    }
}
```

##### Failed Response:
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
        "schemas": {
            "requestBody": {
                "title": "ContactMessageCreationForm",
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "maxLength": 10000,
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

## Docs

https://github.com/jsexton-portfolio/portfolio-documentation/tree/master/web-api
