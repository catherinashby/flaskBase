from flaskBase import create_app
import pytest

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True
    })

    return app
