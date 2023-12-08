from conduit_commons.enums.timeline_events_enum import TimelineEventsEnum
from conduit_commons.kafka.payloads.timeline.timeline_base_order_payload import TimelineBasePayload


class TimelineOrderEsignatureSignedPayload(TimelineBasePayload):
    type = TimelineEventsEnum.TIMELINE_ORDER_ESIGNATURE_SIGNED

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
