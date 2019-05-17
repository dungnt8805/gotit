from . import db
import datetime
from marshmallow import fields, Schema

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # likes = db.relationship('users', secondary=BlogLike, lazy='subquery', backref=db.backref('blogs', lazy=True))

    def __init__(self, data):
        self.title = data.get('title')
        self.content = data.get('content')
        self.user_id = data.get('user_id')
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_blogs():
        return Blog.query.all()

    @staticmethod
    def get_one_blog(id):
        return Blog.query.get(id)

    @staticmethod
    def get_blogs_by_user_id(user_id):
        return Blog.query.filter_by(user_id=user_id).all()

class BlogSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
