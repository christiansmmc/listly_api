from datetime import timedelta

import unicodedata

from flaskr.config.db import db
from flaskr.utils import get_current_time


def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')


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
        lazy=True,
        order_by='Item.id'
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

    category = db.relationship('Category', backref='items', lazy=True)


class Category(BaseModel):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class ProductSuggestion(BaseModel):
    __tablename__ = 'product_suggestion'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    normalized_name = db.Column(db.String(255), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    category = db.relationship('Category', backref='product_suggestions', lazy=True)


class RoomAccess(BaseModel):
    __tablename__ = 'room_access'

    id = db.Column(db.Integer, primary_key=True)
    access_code = db.Column(db.String(6), nullable=False, unique=True)
    expiration_date = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: get_current_time() + timedelta(hours=1)
    )
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    room = db.relationship('Room', backref='accesses', lazy=True)
