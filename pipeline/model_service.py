from fashion_classifier.fashion_classifier_model import FashionClassifierModel
from fashion_classifier.data.config import MAPPING, DOWNLOADED_DATA_DIRNAME
from torchvision.datasets import FashionMNIST as TorchFashionMNIST
from fashion_classifier import util

from pubsub import PubSubAPI

model = FashionClassifierModel("artifacts/epoch=0004-validation.loss=0.220.ckpt")

subscriber_args = {
    "broker_type": "Kafka",
    "client_type": "subscriber",
    "topic": "images",
}
kafka_subscriber = PubSubAPI(**subscriber_args)

publisher_args = {
    "broker_type": "Kafka",
    "client_type": "publisher",
    "topic": "predictions",
}
kafka_publisher = PubSubAPI(**publisher_args)

for message in kafka_subscriber.receive():
    try:
        # split the message into image and id
        # bytesarray, message_id = message.split(b"message_id:")
        # print(f'Received {message_id}')
        # convert the bytesarray to an image
        image = util.byte_array_to_image(message)
        prediction = model.predict(image)
        # print(f'{message_id} ===> {prediction}')
        print(f'{prediction}')
        kafka_publisher.send(message=prediction)
    except Exception as e:
        print(e)
        print(f'Error in processing message {message}')
