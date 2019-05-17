from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .blog import Blog
from .blog_like import BlogLike
from .user import User
