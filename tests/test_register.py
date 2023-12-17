'''
API-тесты на статус-коды 200/400
API-тесты на разные схемы
Позитивные/Негативные тесты на https://reqres.in/api/register
API-тесты на бизнес-логику:
        проверка, что регистрация невозможна для несозданных пользователей
        проверка, что регистрация возможна только при наличии пароля и email
'''

import random
import string

import jsonschema
import requests
from requests import Response

from utils import *


def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))


def test_register_user_successful():
    user = "https://reqres.in/api/users/1"
    email = requests.get(user).json()["data"]["email"]
    url = "https://reqres.in/api/register"
    schema = load_schema(SUCCESSFUL_REGISTER_USER_PATH)
    new_user = {
        "email": email,
        "password": "12345"}

    result: Response = requests.post(url, new_user)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_register_wrong_user():
    url = "https://reqres.in/api/register"
    schema = load_schema(UNSUCCESSFUL_REGISTER_USER_PATH)
    new_user = {
        "email": random_char(7) + "@gmail.com",
        "password": "12345"
    }

    result: Response = requests.post(url, new_user)

    assert result.status_code == 400
    jsonschema.validate(result.json(), schema)
    assert '{"error":"Note: Only defined users succeed registration"}' in result.text


def test_register_available_user_without_password():
    user = "https://reqres.in/api/users/1"
    email = requests.get(user).json()["data"]["email"]
    url = "https://reqres.in/api/register"
    schema = load_schema(UNSUCCESSFUL_REGISTER_USER_PATH)
    new_user = {
        "email": email}

    result: Response = requests.post(url, new_user)

    assert result.status_code == 400
    jsonschema.validate(result.json(), schema)
    assert '{"error":"Missing password"}' in result.text
