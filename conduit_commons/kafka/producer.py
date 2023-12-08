import json
import logging

from confluent_kafka import Producer

COMMON_PRODUCER = logging.getLogger("CommonProducer")


class CommonProducer:
    def __init__(self, host, key=None, secret=None, security_protocol="SSL"):
        self.key = key
        self.secret = secret
        self.host = host
        self.security_protocol = security_protocol

        config = {"bootstrap.servers": self.host, "security.protocol": self.security_protocol}

        if key and secret:
            config["sasl.username"] = self.key
            config["sasl.password"] = self.secret

        self.producer = Producer(config)

    def __produce__(self, topic, value, uuid=None, **kwargs):
        COMMON_PRODUCER.debug(f"Producing message on {topic}. UUID: {uuid}")
        self.producer.produce(
            topic=topic,
            value=json.dumps(value).encode("utf-8"),
            **kwargs,
        )

    def __flush__(self):
        self.producer.flush()
