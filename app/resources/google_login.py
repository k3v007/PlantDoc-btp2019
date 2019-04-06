from secrets import token_hex

from flask import g, request, url_for
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from app.models.user import UserModel
from app.oauth_app import google


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
        print(vars(google_data))

        user = UserModel.find_by_email(google_data.data['email'])
        if user is None:
            name = google_data.data['name'],
            email = google_data.data['email'],
            password = generate_password_hash(token_hex(16))
            user = UserModel(name=name, email=email, password=password)
            user.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200      # noqa
