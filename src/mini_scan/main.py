from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ScanData, Scans

DATABASE_URL = "postgresql://your_user:your_password@localhost:5432/your_db"

def main():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Example data for insertion
    scan_data_v1 = ScanData(response_bytes_utf8=b"aGVsbG8gd29ybGQ=")
    scan_data_v2 = ScanData(response_str="hello world")

    session.add(scan_data_v1)
    session.add(scan_data_v2)
    session.commit()

    scan_v1 = Scans(
        ip="192.168.1.1",
        port=80,
        service="HTTP",
        timestamp=1672531199,
        data_version=1,
        data_id=scan_data_v1.id,
    )
    scan_v2 = Scans(
        ip="192.168.1.2",
        port=22,
        service="SSH",
        timestamp=1672531200,
        data_version=2,
        data_id=scan_data_v2.id,
    )

    session.add(scan_v1)
    session.add(scan_v2)
    session.commit()
    session.close()

if __name__ == "__main__":
    main()
