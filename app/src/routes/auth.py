import os
import json
from flask import request, Blueprint, g, url_for
from ..models.user import User, UserSchema
from flask import current_app as app
from ..shared.res import custom_response
from ..helpers.facebook_auth import FacebookAuth
from ..shared.authentication import Authentication
from ..helpers.google_auth import GoogleAuth

auth_api = Blueprint('auth_api', __name__)
user_schema = UserSchema()

@auth_api.route('/get-facebook-login-url', methods=['GET'])
def get_facebook_login_url():
    url = FacebookAuth.get_login_url(scope='email',
    response_type='token')
    return custom_response({'url': url}, 200)

@auth_api.route('/facebook/authorized', methods=['GET'])
def facebook_authorized():
    if 'access_token' not in request.args:
        return custom_response({'Missing facebook token'}, 401)
    me = FacebookAuth.get_user_info(request.args['access_token'])
    if 'email' not in me:
        return custom_response({'Missing facebook information'}, 401)
    exists_user = User.get_user_by_email(me['email'])
    if exists_user:
        token = Authentication.generate_token(exists_user.id)
        return custom_response({'token': token, 'account_from': exists_user.account_from}, 200)
    data, error = user_schema.load({'email': me['email'], 'account_from': 'facebook'})
    usr = User(data)
    usr.save()
    token = Authentication.generate_token(usr.id)
    return custom_response({'token': token}, 200)


@auth_api.route('/get-google-login-url', methods=['GET'])
def get_google_login_link():
    google = GoogleAuth.get_google_auth()
    auth_url, state = google.authorization_url(
    GoogleAuth.AUTH_URI, access_type='offline')
    return custom_response({'auth_url': auth_url}, 200)


@auth_api.route('/google/authorized', methods=['GET'])
def google_authorized():
    if 'code' not in request.args:
        return custom_response({'error': "Missing access token"}, 201)
    google = GoogleAuth.get_google_auth(url_for('auth_api.google_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))
    try:
        token = google.fetch_token(
                GoogleAuth.TOKEN_URI,
                client_secret=GoogleAuth.CLIENT_SECRET,
                authorization_response=request.url)
    except HTTPError:
        return custom_response({'error': "Authenticate failed"}, 401)
    google = get_google_auth(token=token)
    resp = google.get(GoogleAuth.USER_INFO)
    if resp.status_code != 200
        return custom_response({'error': "Authenticate failed"}, 401)
    user_data = resp.json()
    email = user_data['email']
    exists_user = User.get_user_by_email(me['email'])
    if exists_user:
        token = Authentication.generate_token(exists_user.id)
        return custom_response({'token': token, 'account_from': exists_user.account_from}, 200)
    data, error = user_schema.load({'email': me['email'], 'account_from': 'facebook'})
    usr = User(data)
    usr.save()
    token = Authentication.generate_token(usr.id)
    return custom_response({'user':"user"}, 200)
