class KafkaCommonError(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        default_message = msg or "Generic Kafka error"
        if args:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(default_message, **kwargs)


class NoTopicsError(KafkaCommonError):
    def __init__(self, msg=None, *args, **kwargs):
        msg = msg or "No topics to consume, set KAFKA_TOPICS environment variable"
        super().__init__(msg, **kwargs)
