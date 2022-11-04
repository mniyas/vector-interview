from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient, NewTopic


from base_pubsub import BasePubSub


class KafkaPubSub(BasePubSub):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = kwargs.get("server", "localhost:9092")
        self.topic = kwargs.get("topic", "test")
        self._producer, self._consumer = None, None
        self._admin = None
        if self.client_type == "producer":
            self._producer = Producer({"bootstrap.servers": self.server})
            self.create_topic()
        else:
            self._consumer = Consumer(
                {"bootstrap.servers": self.server, "group.id": "mygroup", "auto.offset.reset": "earliest"}
            )
            self.create_subscription()

    def list_topics(self) -> None:
        """List all topics."""
        print(self._producer.list_topics())

    def create_topic(self, *args, **kwargs) -> None:
        """Create a topic."""
        if not self._admin:
            self._admin = AdminClient({"bootstrap.servers": self.server})
        topic = NewTopic(self.topic, num_partitions=1, replication_factor=1)
        self._admin.create_topics([topic])

    def delete_topic(self, *args, **kwargs) -> None:
        """Delete a topic."""
        if not self._admin:
            self._admin = AdminClient({"bootstrap.servers": self.server})
        futures = self._admin.delete_topics([self.topic], operation_timeout=30)
        # Wait for operation to finish.
        for topic, f in futures.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} deleted".format(topic))
            except Exception as e:
                print("Failed to delete topic {}: {}".format(topic, e))

    def create_subscription(self, *args, **kwargs) -> None:
        """Create a subscription."""
        self._consumer.subscribe([self.topic])

    def delete_subscription(self, *args, **kwargs) -> None:
        """Delete a subscription."""
        self._consumer.unsubscribe()

    def send(self, message="Test") -> None:
        """Send a message to all subscribers."""
        self._producer.produce(
            self.topic,
            message,
            callback=lambda err, decoded_message, original_message=message: self.delivery_report(  # noqa
                err, decoded_message
            ),
        )
        self._producer.flush()

    def receive(self) -> None:
        """Receive a message from a topic."""
        while True:
            message = self._consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                print("Consumer error: {}".format(message.error()))
                continue
            print("Received message: {}".format(message.value().decode("utf-8")))
            yield message.value().decode("utf-8")

    def delivery_report(self, err, decoded_message):
        """Delivery report handler called on
        successful or failed delivery of the message."""
        if err is not None:
            print("Message delivery failed: {}".format(err))
        else:
            print("Message delivered to {} [{}]".format(decoded_message.topic(), decoded_message.partition()))
