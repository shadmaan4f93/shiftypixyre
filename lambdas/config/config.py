import os
import logging


CONNECTION_KEY = {
    "host": os.environ.get('MONGO_HOST', 'your host'),
    "port": os.environ.get('MONGO_PORT', 27017),
    "username": os.environ.get('MONGO_USERNAME', 'root'),
    "password": os.environ.get('MONGO_PASSWORD', 'password'),
    "authSource": os.environ.get('MONGO_AUTH_SOURCE', 'admin'),
    "db_name": os.environ.get('MONGO_DB_NAME', 'recommendation_engine')
}


MAPBOX_TOKEN = {
    "mapbox_token": os.environ.get('MAPBOX_TOKEN', 'mapboxtoken')
}

DAL_URL = {
    "base_url": os.environ.get(
        'DAL_URL', 'http://dal.dev.shiftpixy.com/api/re'),
    "token": os.environ.get('TOKEN', 'token')
}

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
