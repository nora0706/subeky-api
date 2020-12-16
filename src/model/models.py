from flask.json import dump
from database import db
from flask_marshmallow import Marshmallow

from sqlalchemy.orm.attributes import flag_modified



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(150))
    email = db.Column(db.String(50))
    salt = db.Column(db.String(100))
    created_at = db.Column(db.Text)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))


class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    content = db.Column(db.JSON)
    created_at = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User', backref=db.backref('lists', lazy=True))
    
    def __init__(self, name, description, content, creator):
        self.name = name
        self.description = description
        self.content = content
        self.creator_id = creator

    def update_dict(self, dict):
        for name, value in dict.items():
            if name in self.__dict__:
                setattr(self, name, value)
    def update_content(self, key, value):
        self.content[key]['value'] = value
        flag_modified(self, 'content')


ma = Marshmallow()

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    role = ma.Nested(RoleSchema)


class ListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = List
