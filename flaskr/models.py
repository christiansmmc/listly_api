from flaskr.db import db
from flaskr.utils import get_current_time


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Room(BaseModel):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, default='Lista de compras')
    code = db.Column(db.String(255), unique=True, nullable=False)
    passcode = db.Column(db.String(255), nullable=False, default='0000')
    active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=get_current_time)
    updated_at = db.Column(db.DateTime, default=get_current_time, onupdate=get_current_time)
    deleted_at = db.Column(db.DateTime, nullable=True)

    items = db.relationship(
        'Item',
        backref='room',
        cascade='all',
        lazy=True
    )


class Item(BaseModel):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    checked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_current_time)
    deleted_at = db.Column(db.DateTime, nullable=True)


class Category(BaseModel):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
