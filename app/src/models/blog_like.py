from . import db
import datetime
from marshmallow import fields, Schema
from .user import User

class BlogLike(db.Model):
    __tablename__ = 'blogs_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def __init__(self, data):
        self.user_id = data['user_id']
        self.blog_id = data['blog_id']

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_is_liked(user_id, blog_id):
        return BlogLike.query.filter_by(user_id=user_id, blog_id=blog_id).first()

    @staticmethod
    def get_users_like(blog_id):
        # return User.query.join(BlogLike).filter(BlogLike.id == User.id and BlogLike.blog_id == blog_id).all()
        return User.query.join(BlogLike, BlogLike.user_id == User.id).filter(BlogLike.blog_id==blog_id).all()

class BlogLikeSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    blog_id = fields.Int(required=True)
