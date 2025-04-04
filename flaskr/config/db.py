from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    app.db = db

    from flaskr.models import Room, Item, Category, ProductSuggestion
