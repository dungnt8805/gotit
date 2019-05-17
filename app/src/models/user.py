from . import db
from marshmallow import fields, Schema
import datetime
from .blog import BlogSchema

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    account_from = db.Column(db.String(10))
    full_name = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    occupations = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    blogs = db.relationship("Blog", backref="users", lazy=True)

    def __init__(self, data):
        self.email = data.get('email')
        self.account_from = data.get('account_from')
        self.full_name = data.get('full_name')
        self.phone_number = data.get('phone_number')
        self.occupations = data.get('occupations')
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key != 'email' and key != 'account_from':
                setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_user_by_email(value):
        return User.query.filter_by(email=value).first()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    account_from = fields.Str(required=True)
    full_name = fields.Str(required=False)
    phone_number = fields.Str(required=False)
    occupations = fields.Str(required=False)
    blogs = fields.Nested(BlogSchema, many=True)
