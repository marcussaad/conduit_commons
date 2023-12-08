from unittest import TestCase
from unittest.mock import patch

from conduit_commons.kafka.producer import CommonProducer


class CommonProducerTestCase(TestCase):
    def setUp(self):
        self.producer = CommonProducer

    def instantiated_producer(self, **kwargs):
        return self.producer("host", **kwargs)

    @patch("conduit_commons.kafka.producer.Producer")
    def test_init_required_params(self, mocked_producer):

        # Throws error if required params are not passed
        with self.assertRaises(TypeError):
            self.producer()

        subject = self.instantiated_producer()
        config = {
            "bootstrap.servers": "host",
            "security.protocol": "SSL",
        }

        self.assertEqual(subject.host, "host")
        self.assertEqual(subject.security_protocol, "SSL")
        mocked_producer.assert_called_once_with(config)

    @patch("conduit_commons.kafka.producer.Producer")
    def test_init_extra_params(self, mocked_producer):

        # Throws error if required params are not passed
        with self.assertRaises(TypeError):
            self.producer()

        subject = self.instantiated_producer(key="foo", secret="bar")
        config = {
            "bootstrap.servers": "host",
            "security.protocol": "SSL",
            "sasl.username": "foo",
            "sasl.password": "bar",
        }

        self.assertEqual(subject.host, "host")
        self.assertEqual(subject.security_protocol, "SSL")
        self.assertEqual(subject.key, "foo")
        self.assertEqual(subject.secret, "bar")
        mocked_producer.assert_called_once_with(config)

    @patch("conduit_commons.kafka.producer.COMMON_PRODUCER")
    @patch("conduit_commons.kafka.producer.Producer")
    def test_produce_required(self, _, mock_logging):
        subject = self.instantiated_producer()
        subject.__produce__("topic", "value")
        mock_logging.debug.assert_called_once_with("Producing message on topic. UUID: None")
        subject.producer.produce.assert_called_once_with(topic="topic", value=b'"value"')

    @patch("conduit_commons.kafka.producer.COMMON_PRODUCER")
    @patch("conduit_commons.kafka.producer.Producer")
    def test_produce_optional(self, _, mock_logging):
        subject = self.instantiated_producer()
        subject.__produce__("test_topic", "value", uuid="foo", headers=[("test", "header")])
        mock_logging.debug.assert_called_once_with("Producing message on test_topic. UUID: foo")
        subject.producer.produce.assert_called_once_with(
            topic="test_topic", value=b'"value"', headers=[("test", "header")]
        )
