import atexit
import logging
import os
from datetime import timedelta

import pymysql
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from flaskr.config import db, migration, ma
from flaskr.error_handler import configure_error_handlers
from flaskr.routes.category import categories_bp
from flaskr.routes.health import health_bp
from flaskr.routes.rooms import rooms_bp
from flaskr.routes.rooms_items import rooms_items_bp
from flaskr.scheduler import delete_inactive_rooms, delete_soft_deleted_rooms

# pymysql.install_as_MySQLdb()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

apscheduler_logger = logging.getLogger('apscheduler')
apscheduler_logger.setLevel(logging.WARNING)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)

    configure_extensions(app)
    register_blueprints(app)
    configure_error_handlers(app)
    configure_schedulers(app)
    configure_swagger(app)
    configure_jwt(app)

    return app


def configure_extensions(app):
    db.init_app(app)
    migration.init_app(app)
    ma.init_app(app)


def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(rooms_items_bp)
    app.register_blueprint(categories_bp)


def configure_schedulers(app):
    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(
        func=lambda: delete_inactive_rooms(app),
        trigger=IntervalTrigger(hours=3),
        id='delete_inactive_rooms',
        replace_existing=True
    )
    scheduler.add_job(
        func=lambda: delete_soft_deleted_rooms(app),
        trigger=IntervalTrigger(days=1),
        id='delete_soft_deleted_rooms',
        replace_existing=True
    )

    atexit.register(lambda: scheduler.shutdown())


def configure_swagger(app):
    Swagger(app)


def configure_jwt(app):
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=365)

    JWTManager(app)
