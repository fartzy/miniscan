import os
import json
from google.cloud import pubsub_v1
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the environment variable for the emulator
os.environ["PUBSUB_EMULATOR_HOST"] = os.getenv("PUBSUB_EMULATOR_HOST", "localhost:8085")

# Pub/Sub setup
project_id = os.getenv("PUBSUB_PROJECT_ID", "test-project")
topic_id = os.getenv("PUBSUB_TOPIC_ID", "scan-topic")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_message(data_version, data):
    message = {
        "ip": "192.168.1.1",
        "port": 80,
        "service": "HTTP",
        "timestamp": 1633024800,
        "data_version": data_version,
        "data": data,
    }
    message_json = json.dumps(message)
    future = publisher.publish(topic_path, message_json.encode("utf-8"))
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Example messages
    publish_message(1, {"response_bytes_utf8": "aGVsbG8gd29ybGQ="})
    publish_message(2, {"response_str": "hello world"})
