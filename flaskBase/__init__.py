import os

from flask import Flask
from flaskBase.config import Config

def create_app(test_config=None):
    # create and configure the app
    rp = os.environ.get('ROOT_PATH') or os.path.dirname( os.getcwd() )
    ip = os.environ.get('INSTANCE_PATH') or os.path.join(rp,'instance')
    app = Flask( __name__.split('.')[0]
                ,root_path=rp
                ,instance_path=ip
                ,instance_relative_config=True
                 )
    app.config.from_object(Config)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskBase.db3'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

app = create_app()

import flaskBase.routes

