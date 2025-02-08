import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def is_running_in_docker():
    """Fixture to check if the code is running inside a Docker container."""
    try:
        # Check if we are in docker - this file will exist inside of a running container
        with open('/proc/1/cgroup', 'rt') as f:
            return 'docker' in f.read()
    except FileNotFoundError:
        return False

@pytest.fixture(scope="session", autouse=True)
def load_env(is_running_in_docker):
    """Automatically load environment variables from a .env file if not running in Docker."""
    if not is_running_in_docker:
        load_dotenv()
