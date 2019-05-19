import os
import traceback

from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                fresh_jwt_required, get_jwt_identity,
                                get_raw_jwt, jwt_refresh_token_required,
                                jwt_required)
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from app.blacklist import blacklist
from app.custom import admin_required
from app.models.user import UserModel
from app.schemas.user import UserSchema
from app.utils import IMAGE_DIR_PATH

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


# for user register
class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)
        if UserModel.find_by_email(user.email):
            return {"message": "User already exists"}, 400
        print(user)

        try:
            user.password = generate_password_hash(user.password)
            user.save_to_db()
            user.create_img_dir()
            return {"message": "User created successfully"}, 201
        except:     # noqa
            traceback.print_exc()
            return {"message": "Failed to create the user"}, 500


# for user login
class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("name",))
        user = UserModel.find_by_email(user_data.email)
        if user and user.check_password(user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, 
                    "refresh_token": refresh_token}, 200

        return {"message": "Invalid Credentials."}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        blacklist.add(jti)
        return {"message": f"User id '{user_id}' has been logged out successfully"}, 200


# for admin purposes
class User(Resource):
    @classmethod
    @admin_required
    def get(cls, user_id):
        user = UserModel.find_by_id(_id=user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user_schema.dump(user), 200

    @classmethod
    @admin_required
    @fresh_jwt_required
    def delete(cls, user_id):
        user = UserModel.find_by_id(_id=user_id)
        if not user:
            return {"message": "User not found"}, 404
        if user.id == get_jwt_identity():
            return {"message": "Action forbidden!"}, 403
        user.delete_from_db()
        return {"message": "User successfully deleted."}, 200


class UserList(Resource):
    @classmethod
    @admin_required
    def get(cls):
        users = UserModel.find_all()
        return {"users": user_list_schema.dump(users)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
