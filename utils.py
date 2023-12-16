import json
import os

PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
SCHEMAS_PATH = os.path.join(PROJECT_ROOT_PATH, 'schemas')
GET_SINGLE_USER_PATH = os.path.join(SCHEMAS_PATH, 'get_single_user.json')
POST_CREATE_USER_PATH = os.path.join(SCHEMAS_PATH, 'post_create_user.json')
PUT_CHANGE_USER_PATH = os.path.join(SCHEMAS_PATH, 'put_change_user.json')
PATCH_CHANGE_USER_PATH = os.path.join(SCHEMAS_PATH, 'patch_change_user.json')


def load_schema(filepath):
    with open(filepath) as file:
        schema = json.load(file)
        return schema
