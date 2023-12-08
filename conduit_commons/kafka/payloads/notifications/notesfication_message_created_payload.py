from conduit_commons.enums.notification_types_enum import (
    NotificationTypesEnum,
)
from conduit_commons.kafka.payloads.notifications.notification_base_order_payload import (
    BaseNotificationPayload,
    NotificationBaseMessagePayload,
)


class NotificationNotesficationMessageCreatedPayload(BaseNotificationPayload):
    data: NotificationBaseMessagePayload
    type: NotificationTypesEnum = NotificationTypesEnum.NOTESFICATION_MESSAGE_CREATED

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
