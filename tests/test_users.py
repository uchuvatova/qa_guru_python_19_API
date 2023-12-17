'''
API-тесты на каждый из методов GET/POST/PUT/PATCH/DELETE ручек reqres.in
API-тесты на разные схемы
API-тесты на статус-коды 200/201/204/404
API-тесты c ответом и test_delete_single_user_successfully без ответа
Позитивные/Негативные тесты на https://reqres.in/api/users/{user_id}
'''

import random

import jsonschema
import names
import pytest
import requests
from requests import Response

from utils import *


def test_get_single_user_successful():
    url_list_users = "https://reqres.in/api/users"
    available_user = requests.get(url_list_users).json()["total"]
    url = f"https://reqres.in/api/users/{available_user}"
    schema = load_schema(GET_SINGLE_USER_PATH)

    result: Response = requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_get_single_user_unsuccessful():
    url_list_users = "https://reqres.in/api/users"
    not_available_user = requests.get(url_list_users).json()["total"] + 1
    url = f"https://reqres.in/api/users/{not_available_user}"
    schema = load_schema(GET_SINGLE_USER_NOT_FOUND_PATH)

    result: Response = requests.get(url)

    assert result.status_code == 404
    jsonschema.validate(result.json(), schema)


def test_post_single_user_successful():
    url = "https://reqres.in/api/users"
    schema = load_schema(POST_CREATE_USER_PATH)
    jobs = ["lead", "junior", "middle", "senior"]
    new_user = {"name": names.get_first_name(),
                "job": random.choice(jobs)}

    result: Response = requests.post(url, new_user)

    assert result.status_code == 201
    jsonschema.validate(result.json(),
                        schema)  # чтобы тест прошёл, изменила схему: в схеме ответа на сайте указаны name и job


@pytest.mark.parametrize('id_', [1, 2, 13])
def test_put_single_user_successful(id_):  # баг: можно изменить несуществующего в базе пользователя
    url = f"https://reqres.in/api/users/{id_}"
    schema = load_schema(PUT_CHANGE_USER_PATH)
    jobs = ["lead", "junior", "middle", "senior"]
    new_name = names.get_first_name()
    new_job = random.choice(jobs)
    new_user = {
        "name": new_name,
        "job": new_job
    }

    result: Response = requests.put(url, new_user)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)
    assert new_name, new_job in result.text


@pytest.mark.parametrize('id_', [1, 2, 13])
def test_delete_single_user_successful(id_):  # баг: можно удалить несуществующего в базе пользователя
    url = f"https://reqres.in/api/users/{id_}"

    result: Response = requests.delete(url)

    assert result.status_code == 204
    assert not result.content


@pytest.mark.parametrize('id_', [1, 2, 13])
def test_patch_single_user_successful(id_):  # баг: можно изменить несуществующего в базе пользователя
    url = f"https://reqres.in/api/users/{id_}"
    schema = load_schema(PATCH_CHANGE_USER_PATH)
    jobs = ["lead", "junior", "middle", "senior"]
    new_name = names.get_first_name()
    new_job = random.choice(jobs)
    new_user = {
        "name": new_name,
        "job": new_job
    }

    result: Response = requests.patch(url, new_user)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)
    assert new_name or new_job in result.text
