from conduit_commons.enums.notification_types_enum import (
    NotificationTypesEnum,
)
from conduit_commons.kafka.payloads.notifications.notification_base_order_payload import (
    NotificationBaseFilePayload,
    BaseNotificationPayload,
)


class NotificationCabinetFileUploadedPayload(BaseNotificationPayload):
    data: NotificationBaseFilePayload
    type: NotificationTypesEnum = NotificationTypesEnum.CABINET_FILE_UPLOADED

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
