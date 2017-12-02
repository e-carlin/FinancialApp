import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://banterapiuser:@localhost/' # TODO: Change banterapiuser to be imported from settings
database_name = os.getenv('BANTER_DB_NAME', 'banter')


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('BANTER_SECRET_KEY', 'my_precious') # TODO: The secret key we are currently using isn't actually very good use the method described here https://realpython.com/blog/python/token-based-authentication-with-flask/
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
    PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
    PLAID_SECRET_KEY = os.getenv('PLAID_SECRET_KEY')
    PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
    PLAID_ENV = 'sandbox'

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///example'