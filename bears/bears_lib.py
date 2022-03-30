import enum
import allure
import pytest
import requests
import logging
from http import HTTPStatus
from requests.exceptions import ConnectionError

LOGGER = logging.getLogger(__name__)


class Bear(enum.Enum):
    polar = "POLAR"
    brown = "BROWN"
    black = "BLACK"
    gummy = "GUMMY"


base_url = "http://0.0.0.0:8091"
header = {'Content-Type': 'application/json'}
info_path = "info"
bear_path = "bear"


@allure.step('Get info')
def get_info():
    return requests.get(url=f'{base_url}/{info_path}')


@allure.step('Clean bears')
def clean_bears():
    return requests.delete(url=f'{base_url}/{bear_path}')


@allure.step('Get all bears')
def get_all_bears():
    return requests.get(url=f'{base_url}/{bear_path}')


@allure.step('Get one bear')
def get_one_bear(bear_id):
    return requests.get(url=f'{base_url}/{bear_path}/{bear_id}')


@allure.step('Create new bear')
def create_new_bear(bear_type: Bear, name: str, age: float):
    return requests.post(url=f'{base_url}/{bear_path}',
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
    LOGGER.info('Content is: %s', response.content)


def user_create_bear(bear_type: Bear, name: str, age: float):
    with allure.step('User create simple new bear'):
        response = create_new_bear(bear_type, name, age)
        log_response(response)
    with allure.step('Response code is OK'):
        assert response.status_code == HTTPStatus.OK
    return response


def user_view_all_bears():
    with allure.step('User view bear'):
        response = get_all_bears()
        log_response(response)
        data = response.json()
        allure.attach(str(data), 'BEARS LIST IS', allure.attachment_type.TEXT)
        with allure.step('Response code is OK'):
            assert response.status_code == HTTPStatus.OK
        return data
