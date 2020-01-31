from flaskBase import create_app, setup_logging

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_log_config(set_logpath_env):
    assert setup_logging() == "configured"


def test_index(client):
    assert client.get('index').status_code == 200