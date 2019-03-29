from flask import jsonify
from flask_uploads import configure_uploads, patch_request_class
from marshmallow import ValidationError

from app import api_bp, create_app, jwt
from app.blacklist import blacklist
from app.config import DevelopmentConfig
from app.utils import IMAGE_SET

app = create_app(DevelopmentConfig)
app.register_blueprint(api_bp)

patch_request_class(app, size=10 * 1024 * 1024)  # max upload of 20MB image
configure_uploads(app, IMAGE_SET)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


if __name__ == "__main__":
    app.run()
