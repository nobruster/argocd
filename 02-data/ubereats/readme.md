# Data

The data was created based on the UberEats dataset. Its replication used the ShadowTraffic tool, configured to simulate the merging of data from different systems, only reproducing observed patterns. The goal of this process was to ensure data fidelity and evaluate the performance of the data platform applications in different scenarios. Additionally, the data was enriched with external information to enhance the quality of the analyses.

Shadowtraffic configuration:

```json

{
    "generators": [
        {
            "topic": "users",
            "vars": {
                "user_id": {
                    "_gen": "sequentialInteger",
                    "startingFrom": 1
                }
            },
            "key": {
                "user_id": {
                    "_gen": "var",
                    "var": "user_id"
                }
            },
            "value": {
                "user_id": {
                    "_gen": "var",
                    "var": "user_id"
                },
                "uuid": {
                    "_gen": "uuid"
                },
                "first_name": {
                    "_gen": "string",
                    "expr": "#{Name.firstName}",
                    "locale": ["pt", "BR"]
                },
                "last_name": {
                    "_gen": "string",
                    "expr": "#{Name.lastName}",
                    "locale": ["pt", "BR"]
                },
                "cpf": {
                    "_gen": "string",
                    "expr": "#{numerify '###.###.###-##'}",
                    "locale": ["pt", "BR"]
                },
                "birthday": {
                    "_gen": "formatDateTime",
                    "ms": { "_gen": "uniformDistribution", "bounds": [-2524608000000, 7258118400000] },
                    "format": "yyyy-MM-dd"
                },
                "company_name": {
                    "_gen": "string",
                    "expr": "#{Company.name}",
                    "locale": ["pt", "BR"]
                },
                "job": {
                    "_gen": "string",
                    "expr": "#{Job.title}",
                    "locale": ["pt", "BR"]
                },
                "phone_number": {
                    "_gen": "string",
                    "expr": "#{PhoneNumber.phoneNumber}",
                    "locale": ["pt", "BR"]
                },
                "country": {
                    "_gen": "oneOf",
                    "choices": ["BR"]
                },
                "dt_current_timestamp": {
                    "_gen": "formatDateTime",
                    "ms": { "_gen": "now" },
                    "format": "yyyy-MM-dd HH:mm:ss"
                }
            },
            "localConfigs": {
                "throttleMs": {
                    "_gen": "uniformDistribution",
                    "bounds": [
                        100,
                        1000
                    ]
                },
                "value": {
                    "type": "record",
                    "name": "UserData",
                    "fields": [
                        {
                            "name": "user_id",
                            "type": "long"
                        },
                        {
                            "name": "uuid",
                            "type": "string"
                        },
                        {
                            "name": "first_name",
                            "type": "string"
                        },
                        {
                            "name": "last_name",
                            "type": "string"
                        },
                        {
                            "name": "cpf",
                            "type": "string"
                        },
                        {
                            "name": "birthday",
                            "type": "string"
                        },
                        {
                            "name": "company_name",
                            "type": "string"
                        },
                        {
                            "name": "job",
                            "type": "string"
                        },
                        {
                            "name": "phone_number",
                            "type": "string"
                        },
                        {
                            "name": "country",
                            "type": {
                            "type": "enum",
                            "name": "CountryEnum",
                            "symbols": ["BR"]
                            }
                        },
                        {
                            "name": "dt_current_timestamp",
                            "type": "string"
                        }
                    ]
                }
            }
        },
        {
            "topic": "drivers",
            "vars": {
                "driver_id": {
                    "_gen": "sequentialInteger",
                    "startingFrom": 1
                }
            },
            "key": {
                "driver_id": {
                    "_gen": "var",
                    "var": "driver_id"
                }
            },
            "value": {
                "driver_id": {
                    "_gen": "var",
                    "var": "driver_id"
                },
                "uuid": {
                    "_gen": "uuid"
                },
                "first_name": {
                    "_gen": "string",
                    "expr": "#{Name.firstName}",
                    "locale": ["pt", "BR"]
                },
                "last_name": {
                    "_gen": "string",
                    "expr": "#{Name.lastName}",
                    "locale": ["pt", "BR"]
                },
                "date_birth": {
                    "_gen": "formatDateTime",
                    "ms": { "_gen": "uniformDistribution", "bounds": [-2524608000000, 7258118400000] },
                    "format": "yyyy-MM-dd"
                },
                "city": {
                    "_gen": "string",
                    "expr": "#{Address.city}",
                    "locale": ["pt", "BR"]
                },
                "country": {
                    "_gen": "oneOf",
                    "choices": ["BR"]
                },
                "phone_number": {
                    "_gen": "string",
                    "expr": "#{PhoneNumber.phoneNumber}",
                    "locale": ["pt", "BR"]
                },
                "license_number": {
                    "_gen": "string",
                    "expr": "#{bothify '??#######'}"
                },
                "vehicle_type": {
                    "_gen": "oneOf",
                    "choices": ["Motorcycle", "Car", "Bicycle", "Scooter", "E_Bike", "Walk"]
                },
                "vehicle_make": {
                    "_gen": "string",
                    "expr": "#{Company.name}",
                    "locale": ["pt", "BR"]
                },
                "vehicle_model": {
                    "_gen": "string",
                    "expr": "#{Commerce.productName}",
                    "locale": ["pt", "BR"]
                },
                "vehicle_year": {
                    "_gen": "uniformDistribution",
                    "bounds": [1980, 2024],
                    "decimals": 0
                },
                "vehicle_license_plate": {
                    "_gen": "string",
                    "expr": "#{bothify '???###'}",
                    "locale": ["pt", "BR"]
                },
                "dt_current_timestamp": {
                    "_gen": "formatDateTime",
                    "ms": { "_gen": "now" },
                    "format": "yyyy-MM-dd HH:mm:ss"
                }
            },
            "localConfigs": {
                "throttleMs": {
                    "_gen": "uniformDistribution",
                    "bounds": [
                        100,
                        1000
                    ]
                },
                "value": {
                    "type": "record",
                    "name": "DriverData",
                    "fields": [
                        {
                            "name": "driver_id",
                            "type": "long"
                        },
                        {
                            "name": "uuid",
                            "type": "string"
                        },
                        {
                            "name": "first_name",
                            "type": "string"
                        },
                        {
                            "name": "last_name",
                            "type": "string"
                        },
                        {
                            "name": "date_birth",
                            "type": "string"
                        },
                        {
                            "name": "city",
                            "type": "string"
                        },
                        {
                            "name": "country",
                            "type": {
                            "type": "enum",
                            "name": "CountryEnum",
                            "symbols": ["BR"]
                            }
                        },
                        {
                            "name": "phone_number",
                            "type": "string"
                        },
                        {
                            "name": "license_number",
                            "type": "string"
                        },
                        {
                            "name": "vehicle_type",
                            "type": {
                            "type": "enum",
                            "name": "VehicleTypeEnum",
                            "symbols": ["Motorcycle", "Car", "Bicycle", "Scooter", "E_Bike", "Walk"]
                            }
                        },
                        {
                            "name": "vehicle_make",
                            "type": "string"
                        },
                        {
                            "name": "vehicle_model",
                            "type": "string"
                        },
                        {
                            "name": "vehicle_year",
                            "type": "int"
                        },
                        {
                            "name": "vehicle_license_plate",
                            "type": "string"
                        },
                        {
                            "name": "dt_current_timestamp",
                            "type": "string"
                        }
                    ]
                }
            }
        },
        {
            "topic": "restaurants",
            "vars": {
                "restaurant_id": {
                "_gen": "sequentialInteger",
                "startingFrom": 1
                }
            },
            "key": {
                "restaurant_id": {
                "_gen": "var",
                "var": "restaurant_id"
                }
            },
            "value": {
                "restaurant_id": {
                    "_gen": "var",
                    "var": "restaurant_id"
                },
                "uuid": {
                    "_gen": "uuid"
                },
                "name": {
                    "_gen": "string",
                    "expr": "#{Company.name} Restaurante",
                    "locale": ["pt", "BR"]
                },
                "address": {
                    "_gen": "string",
                    "expr": "#{Address.streetAddress}\n#{Address.city} - #{Address.stateAbbr}\n#{Address.zipCode}",
                    "locale": ["pt", "BR"]
                },
                "city": {
                    "_gen": "string",
                    "expr": "#{Address.city}",
                    "locale": ["pt", "BR"]
                },
                "country": {
                    "_gen": "oneOf",
                    "choices": ["BR"]
                },
                "phone_number": {
                    "_gen": "string",
                    "expr": "#{PhoneNumber.phoneNumber}",
                    "locale": ["pt", "BR"]
                },
                "cuisine_type": {
                    "_gen": "oneOf",
                    "choices": ["Italian", "Chinese", "Japanese", "Mexican", "Indian", "American", "French"]
                },
                "opening_time": {
                    "_gen": "oneOf",
                    "choices": ["08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM"]
                },
                "closing_time": {
                    "_gen": "oneOf",
                    "choices": ["06:00 PM", "08:00 PM", "10:00 PM", "11:00 PM"]
                },
                "average_rating": {
                    "_gen": "uniformDistribution",
                    "bounds": [0.0, 5.0],
                    "decimals": 1
                },
                "num_reviews": {
                    "_gen": "uniformDistribution",
                    "bounds": [0, 10000],
                    "decimals": 0
                },
                "dt_current_timestamp": {
                    "_gen": "formatDateTime",
                    "ms": { "_gen": "now" },
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "cnpj": {
                    "_gen": "string",
                    "expr": "#{numerify '##.###.###/####-##'}",
                    "locale": ["pt", "BR"]
                }
            },
            "localConfigs": {
                "throttleMs": {
                    "_gen": "uniformDistribution",
                    "bounds": [
                        100,
                        1000
                    ]
                },
                "value": {
                    "type": "record",
                    "name": "RestaurantData",
                    "fields": [
                    {
                        "name": "restaurant_id",
                        "type": "long"
                    },
                    {
                        "name": "uuid",
                        "type": "string"
                    },
                    {
                        "name": "name",
                        "type": "string"
                    },
                    {
                        "name": "address",
                        "type": "string"
                    },
                    {
                        "name": "city",
                        "type": "string"
                    },
                    {
                        "name": "country",
                        "type": {
                        "type": "enum",
                        "name": "CountryEnum",
                        "symbols": ["BR"]
                        }
                    },
                    {
                        "name": "phone_number",
                        "type": "string"
                    },
                    {
                        "name": "cuisine_type",
                        "type": {
                        "type": "enum",
                        "name": "CuisineTypeEnum",
                        "symbols": [
                            "Italian", "Chinese", "Japanese", "Mexican",
                            "Indian", "American", "French"
                        ]
                        }
                    },
                    {
                        "name": "opening_time",
                        "type": "string"
                    },
                    {
                        "name": "closing_time",
                        "type": "string"
                    },
                    {
                        "name": "average_rating",
                        "type": "double"
                    },
                    {
                        "name": "num_reviews",
                        "type": "long"
                    },
                    {
                        "name": "dt_current_timestamp",
                        "type": "string"
                    },
                    {
                        "name": "cnpj",
                        "type": "string"
                    }
                    ]
                }
            }
        },
        {
            "topic": "ratings",
            "vars": {
                "rating_id": {
                "_gen": "sequentialInteger",
                "startingFrom": 1
                }
            },
            "key": {
                "rating_id": {
                "_gen": "var",
                "var": "rating_id"
                }
            },
            "value": {
                "rating_id": {
                    "_gen": "var",
                    "var": "rating_id"
                },
                "uuid": {
                    "_gen": "uuid"
                },
                "restaurant_identifier": {
                    "_gen": "sequentialInteger",
                    "startingFrom": 1
                },
                "rating": {
                    "_gen": "uniformDistribution",
                    "bounds": [1, 5],
                    "decimals": 0
                },
                "timestamp": {
                    "_gen": "formatDateTime",
                    "ms": {
                        "_gen": "uniformDistribution",
                        "bounds": [1609459200000, { "_gen": "now" }]
                },
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "dt_current_timestamp": {
                    "_gen": "formatDateTime",
                    "ms": { "_gen": "now" },
                    "format": "yyyy-MM-dd HH:mm:ss"
                }
            },
            "localConfigs": {
                "throttleMs": {
                    "_gen": "uniformDistribution",
                    "bounds": [
                        100,
                        1000
                    ]
                },
                "value": {
                    "type": "record",
                    "name": "RatingData",
                    "fields": [
                        {
                            "name": "rating_id",
                            "type": "long"
                        },
                        {
                            "name": "uuid",
                            "type": "string"
                        },
                        {
                            "name": "restaurant_identifier",
                            "type": "long"
                        },
                        {
                            "name": "rating",
                            "type": "int"
                        },
                        {
                            "name": "timestamp",
                            "type": "string"
                        },
                        {
                            "name": "dt_current_timestamp",
                            "type": "string"
                        }
                    ]
                }
            }
        },
        {
            "topic": "orders",
            "vars": {
                "order_id": {
                    "_gen": "sequentialInteger",
                    "startingFrom": 1
                }
            },
            "key": {
                "order_id": {
                    "_gen": "var",
                    "var": "order_id"
                }
            },
            "value": {
                "order_id": {
                    "_gen": "var",
                    "var": "order_id"
                },
                "user_key": {
                    "_gen": "sequentialInteger",
                    "startingFrom": 1
                },
                "restaurant_key": {
                    "_gen": "sequentialInteger",
                    "startingFrom": 1
                },
                "driver_key": {
                    "_gen": "sequentialInteger",
                    "startingFrom": 1
                },
                "order_date": {
                "_gen": "formatDateTime",
                "ms": {
                    "_gen": "uniformDistribution",
                    "bounds": [1609459200000, { "_gen": "now" }]
                },
                "format": "yyyy-MM-dd HH:mm:ss"
                },
                "total_amount": {
                    "_gen": "uniformDistribution",
                    "bounds": [5.0, 100.0],
                    "decimals": 2
                },
                "payment_id": {
                    "_gen": "uuid"
                },
                "dt_current_timestamp": {
                    "_gen": "formatDateTime",
                    "ms": { "_gen": "now" },
                    "format": "yyyy-MM-dd HH:mm:ss"
                }
            },
            "localConfigs": {
                "throttleMs": {
                    "_gen": "uniformDistribution",
                    "bounds": [
                        100,
                        1000
                    ]
                },
                "value": {
                    "type": "record",
                    "name": "OrderData",
                    "fields": [
                        {
                            "name": "order_id",
                            "type": "long"
                        },
                        {
                            "name": "user_key",
                            "type": "long"
                        },
                        {
                            "name": "restaurant_key",
                            "type": "long"
                        },
                        {
                            "name": "driver_key",
                            "type": "long"
                        },
                        {
                            "name": "order_date",
                            "type": "string"
                        },
                        {
                            "name": "total_amount",
                            "type": "string"
                        },
                        {
                            "name": "payment_id",
                            "type": "string"
                        },
                        {
                            "name": "dt_current_timestamp",
                            "type": "string"
                        }
                    ]
                }
            }
        },
        {
            "topic": "order-status",
            "vars": {
                "status_id": {
                "_gen": "sequentialInteger",
                "startingFrom": 1
                }
            },
            "key": {
                "status_id": {
                "_gen": "var",
                "var": "status_id"
                }
            },
            "value": {
                "status_id": {
                    "_gen": "var",
                    "var": "status_id"
                },
                "order_identifier": {
                    "_gen": "sequentialInteger",
                    "startingFrom": 1
                },
                "status": {
                    "_gen": "oneOf",
                    "choices": ["In Analysis", "Accepted", "Preparing", "Ready for Pickup", "Picked Up", "Out for Delivery","Delivered","Completed"]
                },
                "status_timestamp": {
                    "_gen": "formatDateTime",
                    "ms": { "_gen": "now" },
                    "format": "yyyy-MM-dd HH:mm:ss" 
                },
                "dt_current_timestamp": {
                    "_gen": "formatDateTime",
                    "ms": { "_gen": "now" },
                    "format": "yyyy-MM-dd HH:mm:ss"
                }
            },
            "localConfigs": {
                "throttleMs": {
                    "_gen": "uniformDistribution",
                    "bounds": [
                        100,
                        1000
                    ]
                },
                "avroSchemaHint": {
                    "key": {
                        "type": "record",
                        "name": "StatusData",
                        "fields": [
                            {
                                "name": "status_id",
                                "type": "int"
                            }
                        ]
                    },
                    "value": {
                        "type": "record",
                        "name": "StatusData",
                        "fields": [
                            {
                                "name": "status_id",
                                "type": "int" 
                            },
                            {
                                "name": "order_identifier",
                                "type": "int"
                            },
                            {
                                "name": "status",
                                "type": "string"
                            },
                            {
                                "name": "status_timestamp",
                                "type": "string" 
                            },
                            {
                                "name": "dt_current_timestamp",
                                "type": "string" 
                            }
                        ]
                    }
                }
            }
        }
    ],
    "connections": {
        "localKafka": {
            "kind": "kafka",
            "producerConfigs": {
                "bootstrap.servers": "dev-cluster-kafka-bootstrap.ingestion:9092",
                "schema.registry.url": "http://confluent-schema-registry-cp-schema-registry.ingestion:8081",
                "key.serializer": "io.confluent.kafka.serializers.KafkaAvroSerializer",
                "value.serializer": "io.confluent.kafka.serializers.KafkaAvroSerializer"
            }
        }
    }
}
```