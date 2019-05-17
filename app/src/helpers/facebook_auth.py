import os
import facebook
import requests
import json

class FacebookAuth():
    authorize_url='https://graph.facebook.com/oauth/authorize'
    client_id = os.getenv('FACEBOOK_APP_ID')
    client_secret=os.getenv('FACEBOOK_APP_SECRET')
    redirect_url=os.getenv('FACEBOOK_APP_REDIRECT')

    @staticmethod
    def get_login_url(scope, response_type):
        url = FacebookAuth.authorize_url
        url += '?scope='+scope
        url += '&response_type=' + response_type
        url += '&redirect_uri='+FacebookAuth.redirect_uri
        url += '&client_id='+FacebookAuth.client_id
        return url

    @staticmethod
    def get_user_info(token):
        graph = facebook.GraphAPI(access_token=token, version="2.8")
        me = graph.get_object("/me?fields=id,email")
        return me
