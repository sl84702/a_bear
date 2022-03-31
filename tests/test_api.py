import json
import allure
import pytest
import bears.bears_lib as bears
# from bears.bears_lib import *


@allure.step('Cleanup')
@pytest.fixture(scope='function')
def cleanup(http_service):
    bears.clean_bears()
    yield
    bears.clean_bears()


@allure.feature('INFO')
@allure.title('User can get info requests')
@pytest.mark.info
def test_get_info(cleanup):
    with allure.step('User get info requests'):
        response = bears.get_info()
    bears.check_response_ok(response)
    with allure.step('And information is correctly'):
        assert response.content.decode("utf-8") == bears.info



@allure.feature('CREATE')
@allure.title('User can create several correct bear')
@pytest.mark.create
@pytest.mark.parametrize('bear_type, bear_name, bear_age, bear_count', [
    pytest.param(bears.Bear.polar, 'UMKA', 10.1, 10),
    pytest.param(bears.Bear.brown, 'BROWNBEAR', 11.2, 10),
    pytest.param(bears.Bear.black, 'BLACKBEAR', 12.3, 10),
    pytest.param(bears.Bear.gummy, 'GUMMYBEAR', 13.4, 10, marks=pytest.mark.xfail(reason="Bug", strict=True))
])
def test_user_can_create_several_bear(cleanup, bear_type, bear_name, bear_age, bear_count):
    for bear in range(bear_count):
        bears.user_create_bear(bear_type, bear_name, bear_age)

    all_bears = bears.user_view_all_bears()
    with allure.step('Counting bears'):
        assert len(all_bears) == bear_count

    for bear in all_bears:
        bears.check_bear(bear, bear_type, bear_name, bear_age)


@allure.feature('DELETE')
@allure.title('User can delete all bears if bear count is 1')
@pytest.mark.delete
@pytest.mark.parametrize('bear_type, bear_name, bear_age', [
    pytest.param(bears.Bear.polar, 'UMKA', 10.1)
])
def test_user_can_delete_all_bears_bear_count_1(cleanup, bear_type, bear_name, bear_age):
    bears.user_create_bear(bear_type, bear_name, bear_age)
    bears.user_clean_all_bears()
    all_bears = bears.user_view_all_bears()
    with allure.step('There should only be 0 bears'):
        assert len(all_bears) == 0


@allure.feature('DELETE')
@allure.title('User can delete several bears one by one')
@pytest.mark.delete
@pytest.mark.parametrize('bear_type, bear_name, bear_age, bear_count', [
    pytest.param(bears.Bear.polar, 'UMKA', 10.1, 10)
])
def test_user_can_delete_several_bears_one_by_one(cleanup, bear_type, bear_name, bear_age, bear_count):
    for bear in range(bear_count):
        bears.user_create_bear(bear_type, bear_name, bear_age)

    all_bears = bears.user_view_all_bears()
    for bear in all_bears:
        bears.user_delete_one_bear(bear["bear_id"])

    all_bears = bears.user_view_all_bears()
    with allure.step('There should only be 0 bears'):
        assert len(all_bears) == 0


@allure.feature('UPDATE')
@allure.title('User can update several bears age one by one')
@pytest.mark.update
@pytest.mark.parametrize('bear_type, bear_name, bear_age, bear_count', [
    pytest.param(bears.Bear.polar, 'UMKA', 10.1, 10, marks=pytest.mark.xfail(reason="Bug", strict=True))
])
def test_user_can_update_several_bears_age(cleanup, bear_type, bear_name, bear_age, bear_count):
    new_age = 20.2
    for bear in range(bear_count):
        bears.user_create_bear(bear_type, bear_name, bear_age)

    all_bears = bears.user_view_all_bears()
    for bear in all_bears:
        bears.user_update_bear(bear["bear_id"], bear_type, bear_name, new_age)
        got_bear = bears.user_get_one_bear(bear["bear_id"])
        bear_data = json.loads(got_bear.content.decode("utf-8"))
        bears.check_bear(bear_data, bear_type, bear_name, new_age)


@allure.feature('UPDATE')
@allure.title('User can update several bears name one by one')
@pytest.mark.update
@pytest.mark.parametrize('bear_type, bear_name, bear_age, bear_count', [
    pytest.param(bears.Bear.polar, 'UMKA', 10.1, 10)
])
def test_user_can_update_several_bears_name(cleanup, bear_type, bear_name, bear_age, bear_count):
    new_name = "NIDA"
    for bear in range(bear_count):
        bears.user_create_bear(bear_type, bear_name, bear_age)

    all_bears = bears.user_view_all_bears()
    for bear in all_bears:
        bears.user_update_bear(bear["bear_id"], bear_type, new_name, bear_age)
        got_bear = bears.user_get_one_bear(bear["bear_id"])
        bear_data = json.loads(got_bear.content.decode("utf-8"))
        bears.check_bear(bear_data, bear_type, new_name, bear_age)


@allure.feature('UPDATE')
@allure.title('User can update several bears type one by one')
@pytest.mark.update
@pytest.mark.parametrize('bear_type, bear_name, bear_age, bear_count', [
    pytest.param(bears.Bear.polar, 'UMKA', 10.1, 10, marks=pytest.mark.xfail(reason="Bug", strict=True))
])
def test_user_can_update_several_bears_type(cleanup, bear_type, bear_name, bear_age, bear_count):
    new_type = bears.Bear.brown
    for bear in range(bear_count):
        bears.user_create_bear(bear_type, bear_name, bear_age)

    all_bears = bears.user_view_all_bears()
    for bear in all_bears:
        bears.user_update_bear(bear["bear_id"], new_type, bear_name, bear_age)
        got_bear = bears.user_get_one_bear(bear["bear_id"])
        bear_data = json.loads(got_bear.content.decode("utf-8"))
        bears.check_bear(bear_data, new_type, bear_name, bear_age)


@allure.feature('READ')
@allure.title('User can get information about many bears')
@pytest.mark.read
@pytest.mark.parametrize('bear_type, bear_name, bear_age, bear_count', [
    pytest.param(bears.Bear.polar, 'UMKA', 10.1, 10)
])
def test_can_get_info_about_many_bears(cleanup, bear_type, bear_name, bear_age, bear_count):
    for bear in range(bear_count):
        bears.user_create_bear(bear_type, bear_name, bear_age)

    all_bears = bears.user_view_all_bears()

    for bear in all_bears:
        got_bear = bears.user_get_one_bear(bear["bear_id"])
        bear_data = json.loads(got_bear.content.decode("utf-8"))
        bears.check_bear(bear_data, bear_type, bear_name, bear_age)
