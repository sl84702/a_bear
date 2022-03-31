import os
import pytest
import allure
import bears.bears_lib as bears


@allure.step('Wait docker service')
@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    docker_services.wait_until_responsive(
        timeout=10.0, pause=0.1, check=lambda: bears.is_responsive(url=f'{bears.base_url}/{bears.info_path}')
    )
    return bears.base_url


@pytest.fixture(scope="session")
@allure.step('Go to docker-compose')
def docker_compose_file(pytestconfig):
    """Go to docker-compose file."""
    return os.path.join(str(pytestconfig.rootdir), "tests", "docker-compose.yml")
