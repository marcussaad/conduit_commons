from conduit_commons.enums.message_events_enum import MessageTypesEnum
from conduit_commons.kafka.payloads.messages.message_base_order_payload import (
    MessageBaseOrderPayload,
    BaseMessagePayload,
)


class MessageOrderCreatedPayload(BaseMessagePayload):
    data: MessageBaseOrderPayload
    type = MessageTypesEnum.ORDER_CREATED

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
