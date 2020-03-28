import os, logging, json
from logging.config import dictConfig
from flask import Flask, render_template
from flaskBase.config import Config
from flaskBase.db import init_app as db_init

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='FLASKBASE_LOG_CFG'
):  ## set up logging configuration

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        dictConfig(config)
        return "configured"
    return "unchanged"

def create_app(test_config=None):
    # create and configure the app
    rp = os.environ.get('FLASKBASE_ROOT') or os.path.dirname( os.getcwd() )
    ip = os.environ.get('FLASKBASE_INSTANCE') or os.path.join(rp,'instance')
    app = Flask( __name__.split('.')[0]
                ,instance_path=ip
                ,instance_relative_config=True
                 )
    app.config.from_object(Config)

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

    db_init(app)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template( 'frontpage.html' )

    return app

setup_logging()
app = create_app()
