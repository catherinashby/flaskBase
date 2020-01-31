import os, pytest
from flaskBase import create_app

@pytest.fixture
def set_logpath_env(monkeypatch):
    path = os.path.join(os.getcwd(),"tests","data","logging.json")
    monkeypatch.setenv("FLASKBASE_LOG_CFG",path)

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    return app
