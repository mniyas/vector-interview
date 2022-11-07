from torchvision.datasets import FashionMNIST as TorchFashionMNIST
from fashion_classifier.data.config import DOWNLOADED_DATA_DIRNAME
from pubsub import PubSubAPI
import json
import os
import util
import time
import random

# Get FashionMNIST test data
data = TorchFashionMNIST(DOWNLOADED_DATA_DIRNAME, train=False, download=True)

# # Create a Google PubSub publisher
# args = {
#     "broker_type": "GooglePubSub",
#     "client_type": "publisher",
#     "topic": "images",
#     "project_id": "vector-interview-367721",
# }
# Create a Kafka Publisher
args = {
    "broker_type": "Kafka",
    "client_type": "publisher",
    "topic": "images",
    "server": os.environ.get("KAFKA_SERVER", "localhost:9092"),
}
publisher = PubSubAPI(**args)


def send_images() -> None:
    # Send the first 10 images to the topic
    for i in range(10):
        image = data[i][0]
        base64_image = util.image_to_base64(image)
        message = {
            "image": base64_image,
            "id": util.get_random_id(),
        }
        encoded_msg = json.dumps(message, cls=util.BytesEncoder)
        publisher.send(message=encoded_msg)
        time.sleep(random.random())


if __name__ == "__main__":
    send_images()
