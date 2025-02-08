import os
import base64
import json

from google.cloud import pubsub_v1
from sqlalchemy import create_engine, sessionmaker
from sqlalchemy.orm import scoped_session

from models import Base, ScanData, Scans

# Database setup
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
Session = scoped_session(sessionmaker(bind=engine))

# Pub/Sub setup
PUBSUB_PROJECT_ID = os.getenv("PUBSUB_PROJECT_ID")
PUBSUB_SUBSCRIPTION = "scan-sub"
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PUBSUB_PROJECT_ID, PUBSUB_SUBSCRIPTION)


def process_message(message):
    session = Session()
    try:
        data = json.loads(message.data)
        ip = data["ip"]
        port = data["port"]
        service = data["service"]
        timestamp = data["timestamp"]
        data_version = data["data_version"]

        if data_version == 1:
            response_str = base64.b64decode(
                data["data"]["response_bytes_utf8"]
            ).decode("utf-8")
        elif data_version == 2:
            response_str = data["data"]["response_str"]
        else:
            raise ValueError("Unknown data version")

        # Check if the scan already exists
        scan = session.query(Scans).filter_by(ip=ip, port=port, service=service).first()
        if scan:
            # Update existing scan
            scan.timestamp = timestamp
            scan.data_version = data_version
            scan.data.response_str = response_str
        else:
            # Create new scan and scan data
            scan_data = ScanData(response_str=response_str)
            session.add(scan_data)
            session.flush()  # To get the scan_data.id

            scan = Scans(
                ip=ip,
                port=port,
                service=service,
                timestamp=timestamp,
                data_version=data_version,
                data_id=scan_data.id,
            )
            session.add(scan)

        session.commit()
        message.ack()
    except Exception as e:
        print(f"Error processing message: {e}")
        session.rollback()
    finally:
        session.close()


def main():
    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=process_message
    )
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()


if __name__ == "__main__":
    main()
