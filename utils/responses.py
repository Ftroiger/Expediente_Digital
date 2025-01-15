import random
from typing import Any, Dict, Optional, Type, get_origin, get_args
from pydantic import BaseModel
from datetime import datetime

def generate_example(schema: BaseModel) -> BaseModel:
    example_data = {}
    for field, field_info in schema.model_fields.items():
        if field_info.is_required():
            annotation_origin = get_origin(field_info.annotation)

            if annotation_origin == list:
                sub_model = get_args(field_info.annotation)[0]

                if isinstance(sub_model, type) and issubclass(sub_model, BaseModel):
                    example_data[field] = [generate_example(sub_model).model_dump()]
                else:
                    example_data[field] = [sub_model()]

            elif field_info.annotation == datetime:
                example_data[field] = datetime.now()

            elif field_info.annotation == str:
                if field in ["fechaCreacion", "fechaModificacion"]:
                    example_data[field] = str(datetime.now().isoformat())
                else:
                    example_data[field] = f"Example {field}"

            elif field_info.annotation == int:
                example_data[field] = 123

            elif field_info.annotation == float:
                example_data[field] = 123.45

            elif field_info.annotation == bool:
                example_data[field] = random.choice([True, False])

            elif isinstance(field_info.annotation, type) and issubclass(field_info.annotation, BaseModel):
                example_data[field] = generate_example(field_info.annotation).model_dump()
            
            elif field_info.annotation == Optional[datetime]:
                example_data[field] = None
            
            elif field_info.annotation == Optional[int]:
                example_data[field] = None

            else:
                example_data[field] = f"{field_info.annotation.__name__}"
        else:
            example_data[field] = (
                field_info.default_factory()
                if field_info.default_factory
                else "default_value"
            )

    return schema.model_validate(example_data)


def generate_response(
        type: str, schema: Optional[Type[BaseModel]] = None, column: Optional[str] = None
) -> Dict[int, Dict[str, Any]]:
    
    match type:
        case "get_all":
            example_instance = generate_example(schema)
            return {
                200: {
                    "description": "Operación exitosa",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "cantidad_paginas": 1,
                                # column: [example_instance.model_dump()] ,
                                column: [example_instance.model_dump()] if example_instance else [],
                            }
                        }
                    }
                },
                400: {
                    "description": "Solicitud incorrecta",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "No se encontraron registros",
                            }
                        }
                    },
                },
                500: {
                    "description": "Error interno del servidor",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Algo ha salido mal",
                            }
                        }
                    },
                },
            }
        case "get_one":
            example_instance = generate_example(schema)
            return {
                200: {
                    "description": "Operación exitosa",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                column: example_instance.model_dump() if example_instance else [],
                            }
                        }
                    },
                },
                400: {
                    "description": "Solicitud incorrecta",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "No se encontraron registros",
                            }
                        }
                    },
                },
                500: {
                    "description": "Error interno del servidor",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Algo ha salido mal",
                            }
                        }
                    },
                },
            }
        case "post":
            return {
                200: {
                    "description": "Recurso creado exitosamente",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                            }
                        }
                    },
                },
                422: {
                    "description": "Solicitud incorrecta",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Error de solicitud",
                            }
                        }
                    },
                },
                500: {
                    "description": "Error interno del servidor",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Algo ha salido mal",
                            }
                        }
                    },
                },
            }
        case "delete":
            return {
                200: {
                    "description": "Recurso desactivado exitosamente",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                            }
                        }
                    },
                },
                400: {
                    "description": "Solicitud incorrecta",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "No se encontro registro a desactivar",
                            }
                        }
                    },
                },
                422: {
                    "description": "Solicitud incorrecta",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Error de solicitud",
                            }
                        }
                    },
                },
                500: {
                    "description": "Error interno del servidor",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Algo ha salido mal",
                            }
                        }
                    },
                },
            }
        case "put":
            return {
                200: {
                    "description": "Recurso modificado exitosamente",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                            }
                        }
                    },
                },
                422: {
                    "description": "Solicitud incorrecta",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Error de solicitud",
                            }
                        }
                    },
                },
                500: {
                    "description": "Error interno del servidor",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Algo ha salido mal",
                            }
                        }
                    },
                },
            }
        
            
