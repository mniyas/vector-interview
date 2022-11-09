from pubsub import PubSubAPI
import json
import os

# # Create a Google PubSub Subscriber
# args = {
#     "broker_type": "GooglePubSub",
#     "client_type": "subscriber",
#     "topic": "predictions",
#     "project_id": "vector-interview-367721",
#     "subscription_id": "predictions-subscription",
# }
# Create a Kafka Subscriber
args = {
    "broker_type": "Kafka",
    "client_type": "subscriber",
    "topic": "predictions",
    "server": os.environ.get("KAFKA_SERVER", "localhost:9092"),
}
subscriber = PubSubAPI(**args)


def receive_predictions() -> None:
    # Receive the predictions from the subscriber
    for message in subscriber.receive():
        decoded_message = json.loads(message)
        print(decoded_message)


# Run the functions in parallel
if __name__ == "__main__":
    receive_predictions()
