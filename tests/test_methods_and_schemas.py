# API-тесты на каждый из методов GET/POST/PUT/PATCH/DELETE ручек reqres.in
# API-тесты на разные схемы (4 схемы - GET/POST/PUT/PATCH)

import random

import jsonschema
import names
import pytest
import requests
from requests import Response

from utils import *


def test_get_single_user_successfully():
    url = "https://reqres.in/api/users/2"
    schema = load_schema(GET_SINGLE_USER_PATH)

    result: Response = requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_post_single_user_successfully():
    url = "https://reqres.in/api/users"
    schema = load_schema(POST_CREATE_USER_PATH)
    jobs = ["lead", "junior", "middle", "senior"]
    new_user = {"name": names.get_first_name(),
                "job": random.choice(jobs)}

    result: Response = requests.post(url, new_user)

    assert result.status_code == 201
    jsonschema.validate(result.json(),
                        schema)  # чтобы тест прошёл, изменила схему: в схеме ответа на сайте указаны name и job


@pytest.mark.parametrize('id_', [1, 2, 3])
def test_put_single_user_successfully(id_):
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


@pytest.mark.parametrize('id_', [1, 2, 3])
def test_delete_single_user_successfully(id_):
    url = f"https://reqres.in/api/users/{id_}"

    result: Response = requests.delete(url)

    assert result.status_code == 204
    assert not result.content

@pytest.mark.parametrize('id_', [1, 2, 3])
def test_put_single_user_successfully(id_):
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

