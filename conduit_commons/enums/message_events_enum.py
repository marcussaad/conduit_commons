from enum import Enum

import strawberry


@strawberry.enum
class MessageTypesEnum(Enum):
    ORDER_CREATED = "ORDER_CREATED"


class MessageTypesEnumV1:
    @staticmethod
    def get_value(enum: str):
        try:
            return f"{getattr(MessageTypesEnum, enum).value}_V1"
        except AttributeError:
            return None
