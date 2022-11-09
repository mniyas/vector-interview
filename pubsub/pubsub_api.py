from pubsub import KafkaPubSub
from pubsub import GooglePubSub


class PubSubAPI:
    """A unified interface for sending and receiving messages from Kafka or Google PubSub"""

    def __init__(self, broker_type: str = "Kafka", *args, **kwargs):
        if broker_type == "Kafka":
            self._pubsub = KafkaPubSub(*args, **kwargs)
        elif broker_type == "GooglePubSub":
            self._pubsub = GooglePubSub(*args, **kwargs)
        else:
            raise ValueError("Unsupported broker type: {}. Please use 'Kafka' or 'GooglePubSub".format(broker_type))

    def send(self, *args, **kwargs):
        self._pubsub.send(*args, **kwargs)

    def receive(self, *args, **kwargs):
        return self._pubsub.receive(*args, **kwargs)


if __name__ == "__main__":

    # -------------------------- Test kafka --------------------------
    # send message
    args = {
        "broker_type": "Kafka",
        "client_type": "publisher",
        "topic": "test1",
    }
    publisher = PubSubAPI(**args)
    publisher.send(message="Test message for Kafka")
    # receive message
    args["client_type"] = "subscriber"
    subscriber = PubSubAPI(**args)
    for message in subscriber.receive():
        print(message)

    # -------------------------- Test GooglePubSub --------------------------
    # Note: you need to create a Google Cloud project and enable the Pub/Sub API
    # Also, the following code won't execute since the Kafka subscriber is blocking
    # Comment out the above code to test this
    # send message
    args = {
        "broker_type": "GooglePubSub",
        "project_id": "vector-interview",
        "topic_id": "test",
        "subscription_id": "test1",
        "client_type": "publisher",
    }
    publisher = PubSubAPI(**args)
    publisher.send(message="Test message for GooglePubSub")
    # receive message
    args["client_type"] = "subscriber"
    subscriber = PubSubAPI(**args)
    for message in subscriber.receive():
        print(message)
