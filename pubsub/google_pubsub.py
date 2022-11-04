import time
from base_pubsub import BasePubSub
from google.cloud import pubsub_v1
from typing import Callable


class GooglePubSub(BasePubSub):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_id = kwargs.get("project_id", "vector-interview")
        self.topic_id = kwargs.get("topic_id", "test")
        self.subscription_id = kwargs.get("subscription_id", "test1")
        self.publisher, self.subscriber = None, None
        if self.client_type == "producer":
            self.publisher = pubsub_v1.PublisherClient()
            self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)
            # create topic if it doesn't exist
            try:
                self.publisher.get_topic(request={"topic": self.topic_path})
            except Exception:
                self.create_topic()
        else:
            self.subscriber = pubsub_v1.SubscriberClient()
            self.subscription_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)
            self.topic_path = self.subscriber.topic_path(self.project_id, self.topic_id)
            # create subscription if it doesn't exist
            try:
                self.subscriber.get_subscription(request={"subscription": self.subscription_path})
            except Exception as e:
                self.create_subscription()

    def create_subscription(self, *args, **kwargs) -> None:
        """Create a new Pub/Sub subscription."""
        subscription = self.subscriber.create_subscription(
            request={"name": self.subscription_path, "topic": self.topic_path}
        )
        print(f"Created subscription: {subscription.name}")

    def delete_subscription(self, *args, **kwargs) -> None:
        """Delete a Pub/Sub subscription."""
        self.subscriber.delete_subscription(request={"subscription": self.subscription_path})
        print(f"Deleted subscription: {self.subscription_path}")

    def list_topics(self) -> None:
        """List all Pub/Sub topics in the current project."""
        project_path = f"projects/{self.project_id}"
        for topic in self.publisher.list_topics(request={"project": project_path}):
            print(topic)

    def create_topic(self) -> None:
        """Create a new Pub/Sub topic."""
        topic = self.publisher.create_topic(request={"name": self.topic_path})
        print(f"Created topic: {topic.name}")

    def delete_topic(self) -> None:
        """Delete a Pub/Sub topic."""
        self.publisher.delete_topic(request={"topic": self.topic_path})
        print(f"Deleted topic: {self.topic_path}")

    def send(self, message="Test") -> None:
        """Send a message to all subscribers."""
        print("Sending message: {} to topic {}".format(message, self.topic_path))
        future = self.publisher.publish(self.topic_path, data=message.encode("utf-8"))
        future.add_done_callback(self.delivery_report(future, message))

    def receive(self) -> None:
        """Receive a message from a topic."""
        from google.api_core import retry

        while True:
            response = self.subscriber.pull(
                request={"subscription": self.subscription_path, "max_messages": 3},
                retry=retry.Retry(deadline=300),
            )
            if len(response.received_messages) == 0:
                continue
            for message in response.received_messages:
                self.subscriber.acknowledge(
                    request={"subscription": self.subscription_path, "ack_ids": [message.ack_id]}
                )
                yield message.message.data

    def delivery_report(
        self, publish_future: pubsub_v1.publisher.futures.Future, data: str
    ) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
        from concurrent import futures

        def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
            try:
                # Wait 60 seconds for the publish call to succeed.
                print(publish_future.result(timeout=60))
            except futures.TimeoutError:
                print(f"Publishing {data} timed out.")

        return callback
