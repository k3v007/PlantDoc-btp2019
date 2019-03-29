from flask import g, url_for, request
from flask_restful import Resource
from app.oauth_app import google

from app.models.user import UserModel


class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        return google.authorize(url_for("api.google_authorize",
                                        _external=True))


class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        try:
            resp = google.authorized_response()
        except: # noqa
            return {
                "error": request.args["error"],
                "error_description": request.args["error_description"]
            }

        g.access_token = resp['access_token']
        google_data = google.get('userinfo')
        # print(vars(google_data))

        return {"data": google_data.data}, 200
