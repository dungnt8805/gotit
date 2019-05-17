from flask import request, Blueprint, g
from ..models.user import User, UserSchema
from ..models.blog import BlogSchema
from ..shared.res import custom_response
from ..shared.authentication import Authentication

users_api = Blueprint('users_api', __name__)
user_schema = UserSchema()
blog_schema = BlogSchema()

@users_api.route('<int:user_id>', methods=['GET'])
def get_user(user_id):
    usr = User.get_one_user(user_id)
    if not usr:
        return custom_reponse({'error': 'user not found'}, 404)
    data = user_schema.dump(usr).data
    return custom_response(data, 200)

@users_api.route('<int:user_id>/blogs', methods=['GET'])
def get_user_blogs(user_id):
    usr = User.get_one_user(user_id)
    if not usr:
        return custom_reponse({'error': 'user not found'}, 404)
    data = blog_schema.dump(usr.blogs, many=True).data
    return custom_response(data, 200)

@users_api.route('/me', methods=['PUT'])
@Authentication.auth_required
def update():
    req_data = request.get_json()
    usr = User.get_one_user(g.user.id)
    if usr is None:
        return custom_response({'error':'Authorization token Wrong'}, 401)
    if ((usr.account_from == 'facebook' and
        ('phone_number' not in req_data or 'full_name' not in req_data)) or
        (usr.account_from == 'google' and 'occupations' not in req_data)):
        return custom_response({'error': "Missing Information"}, 400)
    data, error = user_schema.load(req_data, partial=True)
    usr.update(data)
    return custom_response(user_schema.dump(usr).data, 200)
