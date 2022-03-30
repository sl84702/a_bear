import os

import pytest
import requests
from bears.bears_lib import *

@allure.step('Wait docker service')
@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    docker_services.wait_until_responsive(
        timeout=10.0, pause=0.1, check=lambda: is_responsive(url=f'{base_url}/{info_path}')
    )
    return base_url

def test_status_code(http_service):
    status = 418
    response = requests.get(http_service + "/status/{}".format(status))

    assert response.status_code == status

@pytest.fixture(scope="session")
@allure.step('Go to docker-compose')
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "tests", "docker-compose.yml")