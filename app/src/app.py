from flask import Flask

from .config import app_config
from .models import db

from .routes.blogs import blogs_api as blogs_blueprint
from .routes.users import users_api as users_blueprint
from .routes.auth import auth_api as auth_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config['config'])

    db.init_app(app)

    app.register_blueprint(blogs_blueprint, url_prefix='/api/blogs')
    app.register_blueprint(users_blueprint, url_prefix='/api/users')
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    @app.route('/', methods=['GET'])
    def index():
        return 'blog api'

    return app
