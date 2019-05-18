import logging

from flask import jsonify
from marshmallow import ValidationError

from app import api_bp, create_app, jwt
from app.blacklist import blacklist

app = create_app()
app.register_blueprint(api_bp)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == "__main__":
    app.run()
