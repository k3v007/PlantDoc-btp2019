from flask import Blueprint, Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.config import Config
from app.models import db
from app.resources.disease import Disease, DiseaseList, RegisterDiseases
from app.resources.image import ImageList, ImageUpload
from app.resources.plant import Plant, PlantList, RegisterPlants
from app.resources.user import (User, UserLogin, UserRegister, UserList,
                                UserLogout)
from app.schemas import ma

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
jwt = JWTManager()


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserLogout, '/logout')
api.add_resource(Plant, '/plant/<string:name>')
api.add_resource(PlantList, '/plants')
api.add_resource(RegisterPlants, '/register/plants')
api.add_resource(Disease, '/disease/<string:name>/<int:plant_id>')
api.add_resource(DiseaseList, '/diseases')
api.add_resource(RegisterDiseases, '/register/diseases')
api.add_resource(ImageUpload, "/upload/image/<string:plant_name>")
api.add_resource(ImageList, "/images")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    return app
