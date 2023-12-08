import logging
import time
from typing import Set

from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

from conduit_commons.kafka.errors import NoTopicsError

COMMON_CONSUMER = logging.getLogger("CommonConsumer")


class CommonConsumer:
    def __init__(
        self,
        host,
        group_id,
        key=None,
        secret=None,
        namespace=None,
        topics=None,
        options=dict,
        logger=None,
        security_protocol="SSL",
    ):

        if not topics:
            raise NoTopicsError

        self.key = key
        self.secret = secret
        self.host = host
        self.namespace = namespace
        self.topics = topics
        self.group_id = group_id
        self.security_protocol = security_protocol

        config = {
            "bootstrap.servers": self.host,
            "group.id": self.group_id,
            "security.protocol": self.security_protocol,
        }

        if key and secret:
            config["sasl.username"] = self.key
            config["sasl.password"] = self.secret

        self.config = config
        self.consumer = Consumer(self.config, logger=logger)

    def topic_to_method(self, topic):
        if topic not in self.topics:
            return None
        return "consume_" + topic.replace(self.namespace, "")

    def subscribe_to_topics(self):

        COMMON_CONSUMER.debug(
            f"Consumer [{self.namespace}] is subscribing to topics {self.topics}.",
            on_assing=lambda: COMMON_CONSUMER.debug("Consumer [{self.namespace}] is now subscribed."),
        )
        self.consumer.subscribe(self.topics)

    def subscriptions(self):
        return self.consumer.assignment()

    def unsubscribe(self):
        if self.consumer.assignment():
            COMMON_CONSUMER.debug(f"Unsubscribing consumer [{self.namespace}]")
            self.consumer.unsubscribe()

    def close(self):
        COMMON_CONSUMER.debug(f"Closing consumer [{self.namespace}]")
        self.consumer.close()

    def poll(self, timeout):
        return self.consumer.poll(timeout=timeout)

    def create_missing_topics(self, topics_list: Set[str]):
        if self.host and self.topics:
            COMMON_CONSUMER.info("Validating all topics to be subscribed to exist")
            admin_client = AdminClient({"bootstrap.servers": self.host, "security.protocol": self.security_protocol})

            existing_topics = set(admin_client.list_topics().topics.keys())

            if existing_topics.intersection(topics_list) != topics_list:
                missing_topics = list(topics_list.difference(existing_topics))

                for missing_topic in missing_topics:
                    COMMON_CONSUMER.info(f"Creating new topic for {missing_topic}")
                    admin_client.create_topics([NewTopic(missing_topic, 1, 1)])

                while not set(missing_topics).issubset([t for t in admin_client.list_topics().topics]):
                    print("Waiting for topic all topics to be created...")
                    time.sleep(0.2)
            else:
                COMMON_CONSUMER.info("All necessary topics already exist")
