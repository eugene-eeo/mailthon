import pytest
import os
from mailthon.middleware import Auth
from mailthon.postman import Postman


SERVER = os.environ['MAILTHON_HOST']
PORT = int(os.environ['MAILTHON_PORT'])
USERNAME = os.environ.get('MAILTHON_USERNAME')
PASSWORD = os.environ.get('MAILTHON_PASSWORD')


@pytest.fixture
def postman():
    middlewares = []
    if USERNAME and PASSWORD:
        middlewares = [
            Auth(USERNAME, PASSWORD)
        ]
    return Postman(
        server=SERVER,
        port=PORT,
        middlewares=middlewares,
        )
