import logging

from flask import jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from app import api_bp, create_app, jwt
from app.blacklist import blacklist
from app.models.user import UserModel

app = create_app()
app.register_blueprint(api_bp)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    current_app.logger.error(err.messages)
    return jsonify(err.messages), 400


@app.errorhandler(AssertionError)
def handle_assertion_error(message):
    current_app.logger.error(message)
    return jsonify({"msg": str(message)}), 400


@app.after_request
def after_request(response):
    user_id = get_jwt_identity()
    if user_id is not None:
        user = UserModel.find_by_id(user_id)
        if user is not None:
            user.ping()

    # Check for login
    if request.endpoint and request.endpoint[-5:] == "login":
        json_body = request.get_json()
        # Ping only if valid data and user
        if "email" in json_body:
            email = json_body["email"]
            if email:
                user = UserModel.find_by_email(email)
                if user:
                    user.ping()

    return response


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@jwt.invalid_token_loader
def no_jwt_provided(decrypted_token):
    return jsonify({"msg": "[BAD] Check your access/refresh token."}), 422


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == "__main__":
    app.run()
