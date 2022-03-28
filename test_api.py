import allure
import pytest
import requests
import json

baseUrl="http://0.0.0.0:8080/"

@allure.feature('INFO')
@allure.title('Get info requests')
@pytest.mark.info
def test_info() :
    path = "info"
    with allure.step('User send get info requests'):
        response = requests.get(url=baseUrl+path)
    with allure.step('Response code is OK'):
        assert response.status_code == 200
