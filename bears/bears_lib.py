import enum
import allure
import requests
import logging
from http import HTTPStatus
from requests.exceptions import ConnectionError

LOGGER = logging.getLogger(__name__)


class Bear(enum.Enum):
    polar = 'POLAR'
    brown = 'BROWN'
    black = 'BLACK'
    gummy = 'GUMMY'


base_url = 'http://0.0.0.0:8091'
header = {'Content-Type': 'application/json'}
info_path = 'info'
bear_path = 'bear'

info = """Welcome to Alaska!
This is CRUD service for bears in alaska.
CRUD routes presented with REST naming notation:

POST			/bear - create
GET			/bear - read all bears
GET			/bear/:id - read specific bear
PUT			/bear/:id - update specific bear
DELETE			/bear - delete all bears
DELETE			/bear/:id - delete specific bear

Example of ber json: {"bear_type":"BLACK","bear_name":"mikhail","bear_age":17.5}.
Available types for bears are: POLAR, BROWN, BLACK and GUMMY."""


@allure.step('Get info')
def get_info():
    """Get information about Alaska service."""
    return requests.get(url=f'{base_url}/{info_path}')


@allure.step('Clean bears')
def clean_bears():
    """Delete all bears from Alaska."""
    return requests.delete(url=f'{base_url}/{bear_path}')


@allure.step('Get all bears')
def get_all_bears():
    """Read all bears from Alaska."""
    return requests.get(url=f'{base_url}/{bear_path}')


@allure.step('Get one bear')
def get_one_bear(bear_id: int):
    """
    Read specific bear

    Args:
        :param bear_id: bear ID in Alaska
    """
    return requests.get(url=f'{base_url}/{bear_path}/{bear_id}')


@allure.step('Delete one bear')
def delete_one_bear(bear_id: int):
    """
    Delete specific bear

    Args:
        :param bear_id: bear ID in Alaska
    """
    return requests.delete(url=f'{base_url}/{bear_path}/{bear_id}')


@allure.step('Create new bear')
def create_new_bear(bear_type: Bear, name: str, age: float):
    """
    Create new bear

    Args:
        :param bear_type: bear type (Available types for bears are: POLAR, BROWN, BLACK and GUMMY)
        :param name: bear name
        :param age: bear age
    """
    return requests.post(url=f'{base_url}/{bear_path}',
                         json={'bear_type': bear_type.value, 'bear_name': name, 'bear_age': age},
                         headers=header)


@allure.step('User update bear')
def update_bear(bear_id: int, bear_type: Bear, name: str, age: float):
    """
    Update existing bear

    Args:
        :param bear_id: bear ID in Alaska
        :param bear_type: bear type (Available types for bears are: POLAR, BROWN, BLACK and GUMMY)
        :param name: bear name
        :param age: bear age
    """
    return requests.put(url=f'{base_url}/{bear_path}/{bear_id}',
                        json={'bear_type': bear_type.value, 'bear_name': name, 'bear_age': age},
                        headers=header)


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == HTTPStatus.OK:
            return True
    except ConnectionError:
        return False


def log_response(response):
    LOGGER.info('Status code is: %s', response.status_code)
    LOGGER.info('Content is: %s', response.content.decode('utf-8'))


def check_response_ok(response):
    log_response(response)
    with allure.step('Response code is OK'):
        assert response.status_code == HTTPStatus.OK, 'Response status code not OK'


@allure.step('User create bear')
def user_create_bear(bear_type: Bear, name: str, age: float):
    """
    User create new bear and check response is OK

    Args:
        :param bear_type: bear type (Available types for bears are: POLAR, BROWN, BLACK and GUMMY)
        :param name: bear name
        :param age: bear age
    """
    with allure.step('User create simple new bear'):
        response = create_new_bear(bear_type, name, age)
    check_response_ok(response)
    return response


@allure.step('User update bear')
def user_update_bear(bear_id: int, bear_type: Bear, name: str, age: float):
    """
    User update existing bear and check response is OK

    Args:
        :param bear_id: bear ID in Alaska
        :param bear_type: bear type (Available types for bears are: POLAR, BROWN, BLACK and GUMMY)
        :param name: bear name
        :param age: bear age
    """
    with allure.step('User update one bear'):
        response = update_bear(bear_id, bear_type, name, age)
    check_response_ok(response)
    return response


@allure.step('User get bear')
def user_get_one_bear(bear_id: int):
    """
    User read specific bear

    Args:
        :param bear_id: bear ID in Alaska
    """
    with allure.step('User get one bear'):
        response = get_one_bear(bear_id)
    check_response_ok(response)
    return response


@allure.step('User delete bear')
def user_delete_one_bear(bear_id: int):
    """
    User delete specific bear

    Args:
        :param bear_id: bear ID in Alaska
    """
    with allure.step('User delete one bear'):
        response = delete_one_bear(bear_id)
    check_response_ok(response)
    return response


@allure.step('User clean all bears')
def user_clean_all_bears():
    """User delete all bears from Alaska."""
    with allure.step('User clean all bears in Alaska'):
        response = clean_bears()
    check_response_ok(response)
    return response


@allure.step('User view all bears')
def user_view_all_bears():
    """User read all bears from Alaska."""
    with allure.step('User view bear'):
        response = get_all_bears()
    check_response_ok(response)
    data = response.json()
    allure.attach(str(data), 'BEARS LIST IS', allure.attachment_type.TEXT)
    return data


@allure.step('Check bear')
def check_bear(bear: dict, bear_type: Bear, bear_name: str, bear_age: float):
    """
    Verify bear fields match expected values

    Args:
        :param bear: bears information
        :param bear_age: bear age
        :param bear_name: bear name
        :param bear_type: bear type (Available types for bears are: POLAR, BROWN, BLACK and GUMMY)
    """
    with allure.step('Bear info should be correct'):
        allure.attach(str(bear), 'Bear info is:', allure.attachment_type.TEXT)
        logging.info(str(bear))
        bear_id = bear['bear_id']
        allure.attach(str(bear_id), 'BEAR ID IS', allure.attachment_type.TEXT)

        resp_type = bear['bear_type']
        allure.attach(str(resp_type), 'BEAR TYPE IS', allure.attachment_type.TEXT)
        assert resp_type == bear_type.value, 'Bear TYPE mismatch'

        resp_name = bear['bear_name']
        allure.attach(str(resp_name), 'BEAR NAME IS', allure.attachment_type.TEXT)
        assert resp_name == bear_name, 'Bear NAME mismatch'

        resp_age = bear['bear_age']
        allure.attach(str(resp_age), 'BEAR AGE IS', allure.attachment_type.TEXT)
        assert resp_age == bear_age, 'Bear AGE mismatch'
