import allure
import pytest
import requests
import json
from http import HTTPStatus

from bears.bears_lib import *


@allure.step('Cleanup')
@pytest.fixture(scope='function')
def cleanup(http_service):
    clean_bears()
    yield
    clean_bears()


@allure.feature('INFO')
@allure.title('Get info requests')
@pytest.mark.info
def test_get_info(cleanup):
    with allure.step('User get info requests'):
        response = get_info()
    with allure.step('Response code is OK'):
        assert response.status_code == HTTPStatus.OK


@allure.feature('CREATE')
@allure.title('User can create simple bear')
@pytest.mark.create
@pytest.mark.parametrize('bear_type, bear_name, bear_age', [
    pytest.param(Bear.polar, 'UMKA', 10.1),
    pytest.param(Bear.brown, 'BROWNBEAR', 11.2),
    pytest.param(Bear.black, 'BLACKBEAR', 12.3),
    pytest.param(Bear.gummy, 'GUMMYBEAR', 13.4),
    pytest.param("UNKNOWN", 'UNKNOWN', 14.5, marks=pytest.mark.xfail)
])
def test_create_one_bear(cleanup, bear_type, bear_name, bear_age):
    # bear_type = Bear.polar
    # bear_name = "Umka"
    # bear_age = 14.1
    with allure.step('User create simple new bear'):
        response = create_new_bear(bear_type, bear_name, bear_age)
        response = create_new_bear(bear_type, bear_name, bear_age)
        response = create_new_bear(bear_type, bear_name, bear_age)
    with allure.step('Response code is OK'):
        assert response.status_code == HTTPStatus.OK
    with allure.step('And bear is is OK'):
        data = response.json()
        allure.attach(str(data), 'DATA IS', allure.attachment_type.TEXT)
        # allure.attach(str(schema(bears)), 'bears IS', allure.attachment_type.TEXT)
        # assert schema(bears) == response
    with allure.step('User view bear'):
        response = get_all_bears()
        data = response.json()
        allure.attach(str(data), 'BEARS LIST IS', allure.attachment_type.TEXT)
        assert response.status_code == HTTPStatus.OK
        for bear in data:
            allure.attach(str(bear), 'one bear', allure.attachment_type.TEXT)
            bear_id = bear["bear_id"]
            allure.attach(str(bear_id), 'BEAR ID IS', allure.attachment_type.TEXT)
            response = get_one_bear(bear_id)
            data_r = response.json()
            allure.attach(str(data_r), 'bears.get_one_bear DATA IS', allure.attachment_type.TEXT)


@allure.feature('DELETE')
@allure.title('User can delete all bears')
@pytest.mark.delete
def test_delete_all_bears(cleanup):
    with allure.step('User view bear'):
        response = get_all_bears()
        data = response.json()
        allure.attach(str(data), 'BEARS LIST IS', allure.attachment_type.TEXT)
        assert response.status_code == HTTPStatus.OK
    with allure.step('User delete all bears'):
        response = clean_bears()
    with allure.step('Response code is OK'):
        assert response.status_code == HTTPStatus.OK
    with allure.step('User view bear'):
        response = get_all_bears()
        data = response.json()
        allure.attach(str(data), 'BEARS LIST IS', allure.attachment_type.TEXT)
        assert response.status_code == HTTPStatus.OK
