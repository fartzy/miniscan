import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.mini_scan.models import Base, ScanData, Scans
from test.conftest import is_running_in_docker, load_env


@pytest.fixture(scope="module")
def engine(is_running_in_docker):
    
    db_host = os.getenv('TEST_POSTGRES_HOST', 'localhost') if is_running_in_docker else 'localhost'

    # Construct the database URL using environment variables
    DATABASE_URL = (
        f"postgresql://{os.getenv('TEST_POSTGRES_USER', 'test_user')}:"
        f"{os.getenv('TEST_POSTGRES_PASSWORD', 'test_password')}@"
        f"{db_host}:"
        f"{os.getenv('TEST_POSTGRES_PORT', '5433')}/"
        f"{os.getenv('TEST_POSTGRES_DB', 'test_db')}"
    )

    return create_engine(DATABASE_URL)

@pytest.fixture(scope="module")
def tables(engine):
    # Ensure tables are created
    Base.metadata.create_all(engine)
    yield
    # Optionally drop tables after tests
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_insert_and_query_scan_data(session):
    # Insert a ScanData record
    scan_data = ScanData(response_str="hello world")
    session.add(scan_data)
    session.commit()

    # Query the ScanData record
    result = session.query(ScanData).filter_by(response_str="hello world").first()
    assert result is not None
    assert result.response_str == "hello world"

def test_insert_and_query_scans(session):
    # Insert a ScanData record
    scan_data = ScanData(response_str="hello world")
    session.add(scan_data)
    session.commit()

    # Insert a Scans record
    scan = Scans(
        ip="192.168.1.1",
        port=80,
        service="HTTP",
        timestamp=1672531199,
        data_version=2,
        data_id=scan_data.id,
    )
    session.add(scan)
    session.commit()

    # Query the Scans record
    result = session.query(Scans).filter_by(ip="192.168.1.1").first()
    assert result is not None
    assert result.ip == "192.168.1.1"
    assert result.data.response_str == "hello world"
