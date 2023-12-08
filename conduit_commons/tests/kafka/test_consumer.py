from unittest import TestCase
from unittest.mock import patch

from conduit_commons.kafka.consumer import CommonConsumer


class CommonConsumerTestCase(TestCase):
    def setUp(self):
        self.consumer = CommonConsumer

    def instantiated_consumer(self):
        return self.consumer(
            "host",
            "group_id",
            namespace="namespace",
            topics=["topic1"],
            options={},
        )

    @patch("conduit_commons.kafka.consumer.Consumer")
    def test_init_required_params(self, mocked_consumer):

        # Throws error if required params are not passed
        with self.assertRaises(TypeError):
            self.consumer()

        subject = self.instantiated_consumer()
        config = {"bootstrap.servers": "host", "group.id": "group_id", "security.protocol": "SSL"}

        self.assertEqual(subject.host, "host")
        self.assertEqual(subject.namespace, "namespace")
        self.assertEqual(subject.topics, ["topic1"])
        # self.assertDictEqual(subject.config, config)
        mocked_consumer.assert_called_once_with(config, logger=None)

    @patch("conduit_commons.kafka.consumer.Consumer")
    def test_topic_to_method(self, _):
        subject = self.instantiated_consumer()
        self.assertEqual(subject.topic_to_method("topic1"), "consume_topic1")

    @patch("conduit_commons.kafka.consumer.Consumer")
    def test_topic_ignore_unknown_topic(self, _):
        subject = self.instantiated_consumer()
        self.assertEqual(subject.topic_to_method("unknown_topic"), None)

    @patch("conduit_commons.kafka.consumer.Consumer")
    def test_subscribe_to_topics(self, _):
        subject = self.instantiated_consumer()
        subject.subscribe_to_topics()
        subject.consumer.subscribe.assert_called_once_with(subject.topics)

    @patch("conduit_commons.kafka.consumer.Consumer")
    def test_subscriptions(self, _):
        subject = self.instantiated_consumer()
        subject.subscriptions()
        subject.consumer.assignment.assert_called_once()

    @patch("conduit_commons.kafka.consumer.Consumer")
    def test_close(self, _):
        subject = self.instantiated_consumer()
        subject.close()
        subject.consumer.close.assert_called_once()

    @patch("conduit_commons.kafka.consumer.Consumer")
    def test_poll(self, _):
        subject = self.instantiated_consumer()
        subject.poll(timeout=1)
        subject.consumer.poll.assert_called_once_with(timeout=1)
