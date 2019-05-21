import os  # noqa

# environment needs to be loaded first
from dotenv import load_dotenv
load_dotenv('.env')

from flask import Blueprint, Flask      # noqa
from flask_cors import CORS     # noqa
from flask_jwt_extended import JWTManager      # noqa
from flask_restful import Api       # noqa

from app.models import db  # noqa
from app.resources import oauth  # noqa
from app.resources.disease import Diseases, DiseasesID     # noqa
from app.resources.google_login import GoogleAuthorize, GoogleLogin  # noqa
from app.resources.image import ImageList, ImageListOfUser, ImageUpload  # noqa
from app.resources.plant import (Plants, PlantsDiseases, PlantsID,  # noqa
                                 PlantsImages)
from app.resources.user import (Login, Logout, TokenRefresh,    # noqa
                                Users, UsersID, UsersImages)
from app.schemas import ma  # noqa


api_bp = Blueprint('api', __name__)
api = Api(api_bp)
jwt = JWTManager()
cors = CORS()


def create_app():

    app = Flask(__name__)

    # app.config.from_object(config_class)
    app.config.from_object(os.environ['APP_SETTINGS'])
    cors.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    # Login related
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(TokenRefresh, "/refresh")
    api.add_resource(GoogleLogin, "/login/google")
    api.add_resource(GoogleAuthorize, "/login/google/authorized",
                                      endpoint="google_authorize")

    # Users
    api.add_resource(Users, '/api/v1/users')
    api.add_resource(UsersID, '/api/v1/users/<int:user_id>')
    api.add_resource(UsersImages, '/api/v1/users/images')

    # Plants
    api.add_resource(Plants, '/api/v1/plants')
    api.add_resource(PlantsID, '/api/v1/plants/<int:plant_id>')
    api.add_resource(PlantsDiseases, '/api/v1/plants/<int:plant_id>/diseases')
    api.add_resource(PlantsImages, '/api/v1/plants/<int:plant_id>/images')

    # Diseases
    api.add_resource(Diseases, '/api/v1/diseases')
    api.add_resource(DiseasesID, '/api/v1/diseases/<int:disease_id>')

    # Image
    api.add_resource(ImageUpload, "/api/upload/image/<int:plant_id>")
    api.add_resource(ImageList, "/api/images")
    api.add_resource(ImageListOfUser, "/api/user/images")

    from app.views import APP
    app.register_blueprint(APP)

    return app
