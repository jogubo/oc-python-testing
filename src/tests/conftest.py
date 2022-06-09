import pytest

import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def clubs():
    return [
        {'name': 'Test Club 1', 'email': 'test1@email', 'points': '20'},
        {'name': 'Test Club 2', 'email': 'test2@email', 'points': '50'},
        {'name': 'Test Club 3', 'email': 'test3@email', 'points': '80'},
    ]


@pytest.fixture
def club(clubs):
    return clubs[0]


@pytest.fixture
def competitions():
    return [
        {
            "name": "Test Competition 1",
            "date": "2020-03-27 10:00:00",
            "places": "25"
        },
        {
            "name": "Test Competition 2",
            "date": "2020-10-22 13:30:00",
            "places": "10"
        }
    ]


@pytest.fixture
def competition(competitions):
    return competitions[0]


@pytest.fixture
def config(mocker, clubs, competitions):
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.competitions', competitions)
