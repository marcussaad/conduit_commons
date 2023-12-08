from datetime import datetime
from typing import Optional, Union

from conduit_commons.enums.message_events_enum import MessageTypesEnum


class MessageBaseOrderPayload:
    order_id: int
    supplier_id: int
    supplier_organization_id: str
    user_id: str
    user_organization_id: str
    user_phone: Optional[str]
    user_email: Optional[str]
    created_at: datetime
    additional_information: Optional[str]

    def __init__(self, *args, **kwargs):
        self.order_id = kwargs.get("order_id")
        self.supplier_id = kwargs.get("supplier_id")
        self.supplier_organization_id = kwargs.get("supplier_organization_id")
        self.user_id = kwargs.get("user_id")
        self.user_organization_id = kwargs.get("user_organization_id")
        self.user_email = kwargs.get("user_email")
        self.user_phone = kwargs.get("user_phone")
        self.created_at = kwargs.get("created_at")
        self.additional_information = kwargs.get("additional_information")

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
            "additional_information": order.additional_information,
        }


class BaseMessagePayload:
    data: Union[MessageBaseOrderPayload]
    type: MessageTypesEnum

    def __init__(self, *args, **kwargs):
        self.data = kwargs.get("data")
