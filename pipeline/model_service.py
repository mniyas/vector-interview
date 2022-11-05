from fashion_classifier.fashion_classifier_model import FashionClassifierModel
import util
import json

from pubsub import PubSubAPI

model = FashionClassifierModel("artifacts/epoch=0004-validation.loss=0.220.ckpt")

# subscriber_args = {
#     "broker_type": "GooglePubSub",
#     "client_type": "subscriber",
#     "topic": "images",
#     "project_id": "vector-interview-367721",
#     "subscription_id": "images-subscription",
# }
subscriber_args = {
    "broker_type": "Kafka",
    "client_type": "subscriber",
    "topic": "images",
}
subscriber = PubSubAPI(**subscriber_args)

# publisher_args = {
#     "broker_type": "GooglePubSub",
#     "client_type": "publisher",
#     "topic": "predictions",
#     "project_id": "vector-interview-367721",
# }
publisher_args = {
    "broker_type": "Kafka",
    "client_type": "publisher",
    "topic": "predictions",
}
publisher = PubSubAPI(**publisher_args)

for message in subscriber.receive():
    try:
        message = json.loads(message)
        image = util.read_b64_image(message["image"])
        prediction = model.predict(image)
        message = {
            "id": message["id"],
            "prediction": prediction,
        }
        publisher.send(message=json.dumps(message))
    except Exception as e:
        print(e)
        print(f"Error in processing message {message}")
