import allure
import pytest
import requests
import json
from http import HTTPStatus
import logging

from bears.bears_lib import *


# LOGGER = logging.getLogger(__name__)

@allure.step('Cleanup')
@pytest.fixture(scope='function')
def cleanup(http_service):
    LOGGER.info("Startup")
    clean_bears()
    yield
    LOGGER.info("Teardown")
    clean_bears()


@allure.feature('INFO')
@allure.title('User can get info requests')
@pytest.mark.info
def test_get_info(cleanup):
    with allure.step('User get info requests'):
        response = get_info()
        log_response(response)
    with allure.step('Response code is OK'):
        assert response.status_code == HTTPStatus.OK


@allure.feature('CREATE')
@allure.title('User can create several correct bear')
@pytest.mark.create
@pytest.mark.parametrize('bear_type, bear_name, bear_age, bear_count', [
    pytest.param(Bear.polar, 'UMKA', 10.1, 10),
    pytest.param(Bear.brown, 'BROWNBEAR', 11.2, 10),
    pytest.param(Bear.black, 'BLACKBEAR', 12.3, 10),
    pytest.param(Bear.gummy, 'GUMMYBEAR', 13.4, 10, marks=pytest.mark.xfail(reason="Bug", strict=True))
])
def test_user_can_create_several_bear(cleanup, bear_type, bear_name, bear_age, bear_count):
    for bear in range(bear_count):
        user_create_bear(bear_type, bear_name, bear_age)

    all_bears = user_view_all_bears()
    with allure.step('Counting bears'):
        assert len(all_bears) == bear_count

    for bear in all_bears:
        check_bear(bear, bear_type, bear_name, bear_age)


@allure.feature('DELETE')
@allure.title('User can delete all bears if bear count is 1')
@pytest.mark.delete
@pytest.mark.parametrize('bear_type, bear_name, bear_age', [
    pytest.param(Bear.polar, 'UMKA', 10.1)
])
def test_user_can_delete_all_bears_bear_count_1(cleanup, bear_type, bear_name, bear_age):
    user_create_bear(bear_type, bear_name, bear_age)
    with allure.step('User delete all bears'):
        response = clean_bears()
        log_response(response)
    with allure.step('Response code is OK'):
        assert response.status_code == HTTPStatus.OK
    all_bears = user_view_all_bears()
    with allure.step('There should only be 0 bears'):
        assert len(all_bears) == 0


@allure.feature('DELETE')
@allure.title('User can delete one bear')
@pytest.mark.delete
def test_user_can_delete_one_bear(cleanup):
    with allure.step('User view bear'):
        response = get_all_bears()


@allure.feature('UPDATE')
@allure.title('User can update bear age to 0')
@pytest.mark.update
def test_can_update_bear_age_to_0(cleanup):
    with allure.step('User view bear'):
        response = get_all_bears()


@allure.feature('READ')
@allure.title('User can get information about many bears')
@pytest.mark.read
@pytest.mark.parametrize('bear_type, bear_name, bear_age, bear_count', [
    pytest.param(Bear.polar, 'UMKA', 10.1, 10)
])
def test_can_get_info_about_many_bears(cleanup, bear_type, bear_name, bear_age, bear_count):
    for bear in range(bear_count):
        user_create_bear(bear_type, bear_name, bear_age)

    all_bears = user_view_all_bears()

    for bear in all_bears:
        got_bear = get_one_bear(bear["bear_id"])
        bear_data = json.loads(got_bear.content.decode("utf-8"))
        check_bear(bear_data, bear_type, bear_name, bear_age)


@allure.feature('READ')
@allure.title('User cannot get information about one bear using invalid id')
@pytest.mark.read
def test_user_cannot_get_info_using_invalid_id(cleanup):
    with allure.step('User view bear'):
        response = get_all_bears()
