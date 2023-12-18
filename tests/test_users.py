import random

import jsonschema
import names
import pytest
import requests
from requests import Response

from utils.load_schema import *


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
    assert '{}' in result.text


def test_post_single_user_successful():
    url = "https://reqres.in/api/users"
    schema = load_schema(POST_CREATE_USER_PATH)
    jobs = ["lead", "junior", "middle", "senior"]
    new_user = {"name": names.get_first_name(),
                "job": random.choice(jobs)}

    result: Response = requests.post(url, new_user)

    assert result.status_code == 201
    jsonschema.validate(result.json(),
                        schema)


@pytest.mark.parametrize('id_', [1, 2, 13])
def test_put_single_user_successful(id_):
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
def test_delete_single_user_successful(id_):
    url = f"https://reqres.in/api/users/{id_}"

    result: Response = requests.delete(url)

    assert result.status_code == 204
    assert not result.content


@pytest.mark.parametrize('id_', [1, 2, 13])
def test_patch_single_user_successful(id_):
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
