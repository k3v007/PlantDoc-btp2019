import os  # noqa

# environment needs to be loaded first
from dotenv import load_dotenv
load_dotenv('.env')

from flask import Blueprint, Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.models import db  # noqa
from app.resources import oauth  # noqa
from app.resources.disease import (Disease, DiseaseList,  # noqa
                                   RegisterDiseases)
from app.resources.google_login import GoogleAuthorize, GoogleLogin  # noqa
from app.resources.image import ImageList, ImageListOfUser, ImageUpload  # noqa
from app.resources.plant import Plant, PlantList, RegisterPlants  # noqa
from app.resources.user import (TokenRefresh, User, UserList,  # noqa
                                UserLogin, UserLogout, UserRegister)
from app.schemas import ma  # noqa


api_bp = Blueprint('api', __name__)
api = Api(api_bp)
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(User, '/api/user/<int:user_id>')
    api.add_resource(UserList, '/api/users')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(TokenRefresh, "/refresh")
    api.add_resource(Plant, '/api/plant/<string:name>')
    api.add_resource(PlantList, '/api/plants')
    api.add_resource(RegisterPlants, '/api/register/plants')
    api.add_resource(Disease, '/api/disease/<string:name>/<int:plant_id>')
    api.add_resource(DiseaseList, '/api/diseases')
    api.add_resource(RegisterDiseases, '/api/register/diseases')
    api.add_resource(ImageUpload, "/api/upload/image/<string:plant_name>")
    api.add_resource(ImageList, "/api/images")
    api.add_resource(ImageListOfUser, "/api/user/images")
    api.add_resource(GoogleLogin, "/login/google")
    api.add_resource(GoogleAuthorize, "/login/google/authorized",
                                      endpoint="google_authorize")                                      

    return app
