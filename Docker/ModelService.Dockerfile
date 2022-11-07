FROM python:3.9-buster

RUN apt update && apt install -y librdkafka-dev

# Create the working directory
#   set -x prints commands and set -e causes us to stop on errors
RUN set -ex && mkdir /repo
WORKDIR /repo
ENV PYTHONPATH ".:"

# Install Python dependencies
COPY requirements/prod.txt ./torch-requirements.txt
COPY requirements/pubsub.txt ./requirements.txt
RUN pip install --default-timeout=100 -r requirements.txt -r torch-requirements.txt
# Install Google PubSub client separately due to dependency conflict
RUN pip install google-cloud-pubsub
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Copy the rest of the code
COPY artifacts/ ./artifacts
COPY fashion_classifier/ ./fashion_classifier
COPY pubsub/ ./pubsub
COPY pipeline/ ./pipeline

ENTRYPOINT ["python", "pipeline/model_service.py"]
