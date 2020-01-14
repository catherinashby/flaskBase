import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #
    #   ENV = 'production'
    #   DEBUG = False
    #   TESTING = False
    #   PROPAGATE_EXCEPTIONS = None
    #   TRAP_HTTP_EXCEPTIONS = False
    #   SECRET_KEY = None
    #   SESSION_COOKIE_NAME = 'session'
    #   SESSION_COOKIE_DOMAIN = None
    #   SESSION_COOKIE_PATH = None
    #   SESSION_COOKIE_HTTPONLY = True
    #   SESSION_COOKIE_SECURE = False
    #   SESSION_COOKIE_SAMESITE = None
    #   PERMANENT_SESSION_LIFETIME = timedelta(days=31) -- 2678400 seconds
    #   SESSION_REFRESH_EACH_REQUEST = True
    #   USE_X_SENDFILE = False
    #   SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=12) -- 43200 seconds
    #   SERVER_NAME = None
    #   APPLICATION_ROOT = '/'
    #   PREFERRED_URl_SCHEME = 'http'
    #   MAX_CONTENT_LENGTH = None
    #   JSON_AS_ASCII = True
    #   JSON_SORT_KEYS = True
    #   JSONIFY_PRETTYPRINT_REGULAR = False
    #   JSONIFY_MIMETYPE = 'application/json'
    #   EXPLAIN_TEMPLATE_LOADING = False
    #   MAX_COOKIE_SIZE = 4093

    #   these values are enabled in DEBUG mode
    #   PRESERVE_CONTEXT_ON_EXCEPTION = None
    #   TRAP_BAD_REQUEST_ERRORS = None
    #   TEMPLATES_AUTO_RELOAD = None

    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    DATABASE = os.environ.get('DATABASE')
