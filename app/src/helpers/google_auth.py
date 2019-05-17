import os
from requests_oauthlib import OAuth2Session


class GoogleAuth:
    CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']
    REDIRECT_URI = os.getenv('GOOGLE_CLIENT_REDIRECT')


    @staticmethod
    def get_google_auth(token=None):
        if token:
            return OAuth2Session(GoogleAuth.CLIENT_ID, token=token)
        oauth = OAuth2Session(
            GoogleAuth.CLIENT_ID,
            redirect_uri = redirect_uri,
            scope = GoogleAuth.SCOPE
        )
        return oauth
