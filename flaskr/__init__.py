import atexit
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask
from flask_migrate import Migrate

from flaskr.db import db
from flaskr.ma import ma
from flaskr.models import Room, Item, Category
from flaskr.routes.health import health_bp
from flaskr.routes.items import items_bp
from flaskr.routes.rooms import rooms_bp
from flaskr.scheduler import delete_inactive_rooms, delete_soft_deleted_rooms

migrate = Migrate()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

apscheduler_logger = logging.getLogger('apscheduler')
apscheduler_logger.setLevel(logging.WARNING)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(items_bp)

    configure_schedulers(app)

    return app


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
