from flaskBase import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_index(client):
    assert client.get('index').status_code == 200