from datetime import datetime
from typing import Optional

from conduit_commons.enums.timeline_events_enum import TimelineEventsEnum


class TimelineBaseStatusPayload:
    status_to: str
    reason: Optional[str] = None
    description: Optional[str] = None

    def __init__(self, *args, **kwargs):
        self.status = kwargs.get("status")
        self.reason = kwargs.get("reason")
        self.description = kwargs.get("description")


class TimelineBaseOrderPayload:
    order_id: int
    # user and supplier id should be optional because we have some events sent from docusign
    # and there we don't have this information, only the user/physician name
    supplier_id: Optional[int] = None
    user_id: Optional[str] = None
    user_organization_id: Optional[int] = None
    user_name: str
    user_phone: Optional[str]
    user_email: Optional[str]
    status_to: TimelineBaseStatusPayload
    created_at: datetime

    def __init__(self, *args, **kwargs):
        self.order_id = kwargs.get("order_id")
        self.supplier_id = kwargs.get("supplier_id")
        self.user_id = kwargs.get("user_id")
        self.user_organization_id = kwargs.get("user_organization_id")
        self.user_name = kwargs.get("user_name")
        self.user_email = kwargs.get("user_email")
        self.user_phone = kwargs.get("user_phone")
        self.status_to = TimelineBaseStatusPayload(**kwargs.get("status_to"))
        self.created_at = kwargs.get("created_at")

    @classmethod
    def create_payload_from_order(cls, order):
        return {
            "order_id": order.id,
            "supplier_id": order.supplier.supplier_id,
            "user_id": order.user.user_id,
            "user_organization_id": order.user.organization_id or 0,
            "user_name": f"{order.user.first_name} {order.user.last_name}",
            "user_email": order.user.email,
            "user_phone": order.user.phone,
            "status_to": TimelineBaseStatusPayload(
                status=order.status,
                # getting last status reason/description if exists
                reason=order.order_status and order.order_status[-1].reason,
                description=order.order_status and order.order_status[-1].description,
            ),
            "created_at": datetime.now(),
        }

    @classmethod
    def create_payload_from_order_and_auth_user(cls, order, auth_user):
        return {
            "order_id": order.id,
            "supplier_id": order.supplier.supplier_id,
            "user_id": auth_user.id(),
            "user_organization_id": auth_user.organization_id() or 0,
            "user_name": f"{auth_user.given_name} {auth_user.family_name}",
            "user_email": auth_user.email,
            "user_phone": auth_user.phone,
            "status_to": TimelineBaseStatusPayload(
                status=order.status,
                reason=order.order_status and order.order_status[-1].reason,
                description=order.order_status and order.order_status[-1].description,
            ),
            "created_at": datetime.now(),
        }

    @classmethod
    def create_payload_from_esignature(cls, order):
        return {
            "order_id": order.id,
            "user_name": f"{order.physician.first_name} {order.physician.last_name}",
            "user_email": order.physician.email,
            "user_phone": order.physician.phone,
            "status_to": TimelineBaseStatusPayload(status=order.esignature.status),
            "created_at": datetime.now(),
        }


class TimelineBasePayload:
    data: TimelineBaseOrderPayload
    type: TimelineEventsEnum

    def __init__(self, *args, **kwargs):
        self.data = kwargs.get("data")
