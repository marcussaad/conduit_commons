from datetime import datetime
from typing import Union, Optional

from conduit_commons.enums.notification_types_enum import NotificationTypesEnum


class NotificationBaseOrderPayload:
    order_id: int
    supplier_id: int
    supplier_organization_id: str
    user_id: str
    user_organization_id: str
    user_phone: Optional[str]
    user_email: Optional[str]
    created_at: datetime

    def __init__(self, *args, **kwargs):
        self.order_id = kwargs.get("order_id")
        self.supplier_id = kwargs.get("supplier_id")
        self.supplier_organization_id = kwargs.get("supplier_organization_id")
        self.user_id = kwargs.get("user_id")
        self.user_organization_id = kwargs.get("user_organization_id")
        self.user_email = kwargs.get("user_email")
        self.user_phone = kwargs.get("user_phone")
        self.created_at = kwargs.get("created_at")

    @classmethod
    def create_payload_from_order(cls, order):
        return {
            "order_id": order.id,
            "supplier_id": order.supplier.supplier_id,
            "supplier_organization_id": order.supplier.organization_id,
            "user_id": order.user.user_id,
            "user_organization_id": order.user.organization_id,
            "user_email": order.user.email,
            "user_phone": order.user.phone,
            "created_at": order.created_at,
        }


class NotificationBaseMessagePayload:
    sender_id: str
    sender_organization_id: str
    recipient_id: Optional[str]
    recipient_organization_id: Optional[str]
    channel: str
    order_id: int

    def __init__(self, *args, **kwargs):
        self.sender_id = kwargs.get("sender_id")
        self.sender_organization_id = kwargs.get("sender_organization_id")
        self.recipient_id = kwargs.get("recipient_id")
        self.recipient_organization_id = kwargs.get("recipient_organization_id")
        self.channel = kwargs.get("channel")
        self.order_id = kwargs.get("order_id")


class NotificationBaseFilePayload:
    filename: str
    uploader_id: str
    order_id: int
    supplier_organization_id: str

    def __init__(self, *args, **kwargs):
        self.filename = kwargs.get("filename")
        self.uploader_id = kwargs.get("uploader_id")
        self.order_id = kwargs.get("order_id")
        self.supplier_organization_id = kwargs.get("supplier_organization_id")


class BaseNotificationPayload:
    data: Union[NotificationBaseOrderPayload, NotificationBaseFilePayload, NotificationBaseMessagePayload]
    type: NotificationTypesEnum

    def __init__(self, *args, **kwargs):
        self.data = kwargs.get("data")
