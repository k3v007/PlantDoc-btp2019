import os

from flask import g

from app.resources import oauth

# Google oauth settings
google = oauth.remote_app(
    'google',
    consumer_key=os.environ['GOOGLE_ID'],
    consumer_secret=os.environ['GOOGLE_SECRET'],
    request_token_params={
        'scope': ['email', 'profile']
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)


@google.tokengetter
def get_google_token():
    if 'access_token' in g:
        return g.access_token
