import jwt
import os
import datetime
from flask import json, request, g
from .res import custom_response
from ..models.user import User, UserSchema
from functools import wraps

user_schema = UserSchema()

class Authentication():
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'user_id': user_id
            }
            return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), 'HS256').decode("utf-8")
        except Exception as e:
            return custom_response({'error': 'generating token error'}, 401)
    @staticmethod
    def decode_token(bearer):
        decoded_token = {'data': {}, 'error': {}}
        try:
            token = bearer.split(" ")[1]
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
            decoded_token['data'] = {'user_id': payload['user_id']}
            return decoded_token
        except jwt.ExpiredSignatureError:
            decoded_token['error'] = {'message': 'token expired, please login again'}
            return docoded_token
        except jwt.InvalidTokenError:
            decoded_token['error'] = {'message': 'Invalid token, please try again with a new token'}
            return decoded_token

    @staticmethod
    def auth_required(func):
        @wraps (func)
        def decorated_auth(*args, **kwargs):
            if 'Authorization' not in request.headers:
                return custom_response({'error': "Missing Authentication token!"}, 401)
            token = request.headers.get('Authorization')
            decoded_token = Authentication.decode_token(token)
            if (decoded_token['error']):
                return custom_response(decoded_token['error'], 401)
            user_id = decoded_token['data']['user_id']
            usr = User.get_one_user(user_id)
            if not usr:
                return custom_response({'error': "invalid token"}, 401)
            g.user = usr
            return func(*args, **kwargs)
        return decorated_auth

    @staticmethod
    def info_required(func):
        @wraps(func)
        def decorated_info(*args, **kwargs):
            usr = g.user
            if ((usr.account_from == 'facebook' and
                (usr.phone_number == '' or usr.full_name =='')) or
                (usr.account_from == 'google' and usr.occupations =='')):
                return custom_response({'error': "Missing information. Please fill your information"}, 401)
            return func(*args, **kwargs)
        return decorated_info
