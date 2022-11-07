# Vector
This is the solution for ML Engineering interview task at [Vector.ai](https://vector.ai/).

## Project Structure
There are 3 parts for the excercise.
- Part 1: Build a CNN based classifier model for FashionMNIST dataset. The code for model is available in `fashion_classifier` folder and the script to train the model is available in `training` folder.
- Part 2: Build a unified programming interface in Python that a developer can use to send and receive messages to / from Apache Kafka and Google PubSub. The code for this is available at `pubsub` folder.
- Part 3: Use the model from Part 1 and the library from Part 2 to build a system to classify images. The system will have a single client consuming a single machine learning service. The code for this is available in `pipeline` folder

## Setup
### Part 1
I have used conda for managing Python and pip-tools for managing Python package dependencies. Follow the below steps to setup repo.
- Install [Anaconda](https://www.anaconda.com/products/distribution)
- Run `make conda-update` to setup the conda environment
- Run `conda activate vector` to activate the project environment
- Run `make pip-tools` to install dependencies
- Run `export PYTHONPATH=.` inside the root folder

### Part 2
To run Kafka I have used Docker image from Confluent.
- Run Kafka using Docker by `docker compose -f docker-compose.yml up -d`

To run GooglePubSub emulator:
- Install the emulator following this [link](https://cloud.google.com/pubsub/docs/emulator)
- Install Google PubSub client separately due to dependency [conflict](https://github.com/Lightning-AI/lightning/issues/9900)
    - `pip install google-cloud-pubsub`
    - `export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`
- Run the emulator by `gcloud beta emulators pubsub start --project=vector-interview-367721`
- Take a note of the port at which emulator is running

Set the Google PubSub env variables:
- `export PUBSUB_EMULATOR_HOST=localhost:PORT_NUMBER`. Note: Replace the PORT_NUMBER from emulator
- `export PUBSUB_PROJECT_ID=vector-interview-367721`

## Run the code
## Part 1
- I have used ResNet architecture to build the classifier which achieved an accuracy of 91.3%.
- I have used [PyTorch](https://pytorch.org/) & [PyTorch Lightning](https://www.pytorchlightning.ai/) to build and train the model.
- The folder structure for this task is given below:
```bash
.
├── fashion_classifier
│   ├── data
│   │   ├── base_data_module.py
│   │   ├── config.py
│   │   ├── fashion_mnist.py
│   │   └── utils.py
│   ├── fashion_classifier_model.py
│   ├── lit_models
│   │   └── base_model.py
│   ├── models
│   │   └── resnet.py
│   └── util.py
└── training
    ├── logs
    ├── run_experiment.py
    └── util.py
```
- The `data` folder defines an abstract data model using `base_data_module`. This defines the data loaders for train, validation and test.
- `data/fashion_mnist.py` inherits the `BaseDataModule` and create a data model by specifying the 'data preperation' and 'setup' methods.
- If a new data source needs to be added, please create a new data module by inheriting the `BaseDataModule`. You will have to override the `prepare_data` and 'setup` methods`. Please have a look at the `FashionMNIST` class to understand further.
- The `lit_models/base_model.py` file defines a base PyTorch Lightning model(BaseLitModel) which defines the optimizer, LR scheduler, loss calculations for training, validation, and testing.
- The `models/resnet.py` inherits the `BaseLitModel` and defines the ResNet architecture.
- The `training/run_experiment.py` defines the script to train the model.
- Run the training by `python training/run_experiment.py --model_class=ResNet --data_class=FashionMNIST --max_epochs=5 --num_workers=4`
- Run `python training/run_experiment.py --model_class=ResNet --data_class=FashionMNIST --help` to see which command line args are available and read their documentation.
- To train the model on a new data set, we just need to create a new data class and pass it as argument to training script. Similarly, a new model class can also be passed as an arugment to train the model with a new architecture.
- `fashion_classifier_model.py` Creates an inference model by taking the best performing model checkpoint and converting it to a [TorchScript](https://pytorch.org/docs/stable/jit.html) model.

## Part 2
- I have created an interfaced called `PubSubAPI`, supporting `send` and `recieve` methods for this task.
- The folder structure for this task is given below:
```bash
.
└── pubsub
    ├── base_pubsub.py
    ├── google_pubsub.py
    ├── kafka_pubsub.py
    └── pubsub_api.py

```
- `base_pubsub.py` implements an abstract class with `send` and `recieve` abstract methods. It takes client_type as an argument, which has to be either "publisher" or "subscriber". By default, it is a "publisher"
- `kafka_pubsub.py` inherit the `BasePubSub` and implement the `send` and `recieve` methods for Kafka. The send method is `async` while the `recieve` method is a synchronous pull based approach. It takes the server, topic and group_id as arguments.
- `google_pubsub.py` inherit the `BasePubSub` and implement the `send` and `recieve` methods for Google PubSub. The send method is `async` while the `recieve` method is a synchronous pull based approach. It takes project_id, topic, subscription_id arguments
- `pubsub_api.py` implements `PubSubAPI` which takes the broker_type as an argument, which could be either "Kafka" or "GooglePubSub". Sample usage of this interface is given in the file itself. Please refer to that.


## Part 3
- I have built an ML Pipeline using Part 1 and Part 2 components. I have used Kafka as broker for the demo, since it is easy to run the emulator with docker. However, the pipeline works with Google PubSub as well.
- The folder structure for this task is given below:
```bash
.
├── fashion_classifier
│   └── fashion_classifier_model.py
└── pipeline
    ├── application_consumer.py
    ├── application_producer.py
    ├── model_service.py
    └── util.py
```
- `application_producer.py` file creates a Publisher using PubSubAPI and send a base64 encoded image and a random message id to a 'images' topic.
- `model_service.py` file creates a Subscriber for 'images' topic and a Producer for 'predictions' topic. The service initlize the Classifier model from `fashion_classifier/fashion_classifier_model.py`. When a message is recieved by Subscriber, it decode the base64 encoded image into PIL Image and send it to model. The returned prediction is send to 'predictions' topic along with the message id in original message.
- `application_consumer.py` file creates a Subscriber for 'predictions' topic. The messages arriving at 'predictions' are printed to the console up on arrival.

# Running the pipeline with Docker
Components of Part 3 can be run using Docker.
### Build Docker images
- `docker build --platform linux/amd64 -f Docker/ModelService.Dockerfile -t vector-model-service:0.0 .`
- `docker build --platform linux/amd64 -f Docker/AppProducer.Dockerfile -t vector-application-producer:0.0 .`
- `docker build --platform linux/amd64 -f Docker/AppConsumer.Dockerfile -t vector-application-consumer:0.0 .`
## Run the images
Please ensure that Kafka is running locally and run the following components.
- `docker run --platform linux/amd64 --rm --tty --net=host --interactive vector-model-service:0.0`
- `docker run --platform linux/amd64 --rm --tty --net=host --interactive vector-application-producer:0.0`
- `docker run --platform linux/amd64 --rm --tty --net=host --interactive vector-application-consumer:0.0`


### Future Work
There are a few additional improvements I could have made with more time.
- Implementing batch inference for model by waiting for maximum number of messages with in a session window and making predictions. This could help in taking advantage of vectorized operations of model.
- Adding Logging instead of printing messages to console
- Containarize Google PubSub emulator with Docker.
- Add integrations tests for the pipeline
