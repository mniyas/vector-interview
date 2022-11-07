FROM python:3.9-buster

RUN apt update && apt install -y librdkafka-dev

# Create the working directory
#   set -x prints commands and set -e causes us to stop on errors
RUN set -ex && mkdir /repo
WORKDIR /repo
ENV PYTHONPATH ".:"

# Install Python dependencies
COPY requirements/pubsub.txt ./requirements.txt
RUN pip install --default-timeout=100 -r requirements.txt

# Copy the rest of the code
# COPY pubsub/ ./pubsub
# COPY pipeline/ ./pipeline

ENTRYPOINT ["python", "pipeline/application_producer.py"]
