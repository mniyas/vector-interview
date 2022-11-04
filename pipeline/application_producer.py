from torchvision.datasets import FashionMNIST as TorchFashionMNIST
from fashion_classifier import util
from fashion_classifier.data.config import DOWNLOADED_DATA_DIRNAME
from pubsub import PubSubAPI
import random
import time

# Get FashionMNIST test data
data = TorchFashionMNIST(DOWNLOADED_DATA_DIRNAME, train=False, download=True)

# Create a Kafka Producer
args = {
    "broker_type": "Kafka",
    "client_type": "publisher",
    "topic": "images",
}
kafka_publisher = PubSubAPI(**args)

# Create a Kafka Consumer
args = {
    "broker_type": "Kafka",
    "client_type": "subscriber",
    "topic": "predictions",
}
kafka_consumer = PubSubAPI(**args)



def send_images() -> None:
    # Send the first 10 images to the Kafka topic
    for i in range(10):
        image = data[i][0]
        bytearray = util.image_to_byte_array(image)
        message_id = util.get_random_id()
        # add the message_id to the message
        # message = bytearray + b"message_id:" + message_id.encode("utf-8")
        message = bytearray
        kafka_publisher.send(message=message)
        time.sleep(random.random())

# Run the functions in parallel
if __name__ == "__main__":
    send_images()