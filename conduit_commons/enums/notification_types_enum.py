import strawberry
from enum import Enum

from conduit_auth.roles.roles import Roles


class NotificationType:
    def __init__(self, name: str, description: str):
        self.name = name
        self.value = name
        self.description = description


@strawberry.enum
class NotificationTypesEnum(Enum):
    ORDER_CREATED = NotificationType(name="ORDER_CREATED", description="New orders received")
    ORDER_REJECTED = NotificationType(name="ORDER_REJECTED", description="Order rejected by supplier")

    NOTESFICATION_MESSAGE_CREATED = NotificationType(
        name="NOTESFICATION_MESSAGE_CREATED", description="New message on an order"
    )

    CABINET_FILE_UPLOADED = NotificationType(name="CABINET_FILE_UPLOADED", description="New file uploaded on an order")

    @classmethod
    def get_notifications_types_for_role(cls, role: Roles):
        if role == Roles.SupplierRole:
            return [cls.ORDER_CREATED, cls.NOTESFICATION_MESSAGE_CREATED, cls.CABINET_FILE_UPLOADED]
        elif role == Roles.MarketplaceUserRole:
            return [cls.ORDER_REJECTED, cls.NOTESFICATION_MESSAGE_CREATED]
        return []


class NotificationTypesEnumV1:
    @staticmethod
    def get_value(enum: str):
        try:
            return f"{getattr(NotificationTypesEnum, enum).value}_V1"
        except AttributeError:
            return None
