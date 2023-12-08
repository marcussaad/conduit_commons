from conduit_commons.enums.notification_types_enum import (
    NotificationTypesEnum,
)
from conduit_commons.kafka.payloads.notifications.notification_base_order_payload import (
    BaseNotificationPayload,
    NotificationBaseOrderPayload,
)


class NotificationOrderCreatedPayload(BaseNotificationPayload):
    data: NotificationBaseOrderPayload
    type = NotificationTypesEnum.ORDER_CREATED

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
