from flask import current_app, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                fresh_jwt_required, get_jwt_identity,
                                get_raw_jwt, jwt_refresh_token_required,
                                jwt_required)
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from app.blacklist import blacklist
from app.custom import admin_required
from app.models.image import ImageModel
from app.models.user import UserModel
from app.schemas.image import ImageModelSchema
from app.schemas.user import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)
image_list_schema = ImageModelSchema(many=True)


# For all users resource
class Users(Resource):
    # Get all the users
    @classmethod
    @admin_required
    def get(cls):
        users = UserModel.find_all()
        return {"users": user_list_schema.dump(users)}, 200

    # Register a user
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)
        if UserModel.find_by_email(user.email):
            current_app.logger.debug(f"Email<{user.email}> already registered")
            return {"msg": "User already registered"}, 400

        if len(user.password) < 4:
            current_app.logger.error(f"Password-len<{len(user.password)}> not allowed")     # noqa
            raise AssertionError("Password length should be greater than 4 characters.")    # noqa

        try:
            user.name = ' '.join([i.capitalize() for i in user.name.split()])
            user.password = generate_password_hash(user.password)
            user.save_to_db()
            current_app.logger.info(f"Registered {user} successfully")
            return {"msg": "You have successfully registered"}, 201
        except Exception as err:     # noqa
            current_app.logger.error(err)
            return {"msg": "Failed to register the user"}, 500


# For user resource by ID
class UsersID(Resource):
    # Get user
    @classmethod
    @admin_required
    def get(cls, user_id):
        user = UserModel.find_by_id(_id=user_id)
        if not user:
            current_app.logger.debug(f"User-id<{user_id}> not found.")
            return {"msg": f"User[id={user_id}] not found"}, 404
        return user_schema.dump(user), 200

    # Update user information
    @classmethod
    @admin_required
    def put(cls, user_id):
        user = UserModel.find_by_id(_id=user_id)
        if not user:
            current_app.logger.debug(f"User-id<{user_id}> not found.")
            return {"msg": f"User[id={user_id}] not found"}, 404

        _user = user_schema.load(request.get_json(),
                                 partial=("email", "password"))
        _user.name = user.name if _user.name is None else _user.name
        _user.active = user.active if _user.active is None else _user.active
        user.name = _user.name
        user.active = _user.active
        try:
            user.save_to_db()
            current_app.logger.info(f"Updated {user}")
            return {"msg": f"User[id={user_id}] info has been successfully updated"}, 201   # noqa
        except Exception as err:     # noqa
            current_app.logger.error(err)
            return {"msg": "Failed to update the user's info"}, 500

    # Delete user
    @classmethod
    @admin_required
    @fresh_jwt_required
    def delete(cls, user_id):
        user = UserModel.find_by_id(_id=user_id)
        if not user:
            current_app.logger.debug(f"User-id<{user_id}> not found.")
            return {"msg": f"User[id={user_id}] not found"}, 404
        if user.id == get_jwt_identity():
            current_app.logger.debug(f"Admin can't delete themselves.")
            return {"msg": "Delete own account not allowed."}, 403
        try:
            user.delete_from_db()
            current_app.logger.info(f"Deleted user<{user}")
            return {"msg": "User has been successfully deleted."}, 200
        except Exception as err:     # noqa
            current_app.logger.error(err)
            return {"msg": "Failed to delete the user"}, 500


# Get all images of a User
class UsersImages(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        query = request.args.get('sort')
        user_id = get_jwt_identity()
        if query is not None:
            if query[0] == '-':
                return {"images": image_list_schema.dump(
                    ImageModel.query.filter_by(user_id=user_id).order_by(
                        ImageModel.upload_date.desc()).all()
                )}, 200
            else:
                return {"images": image_list_schema.dump(
                    ImageModel.query.filter_by(user_id=user_id).order_by(
                        ImageModel.upload_date.asc()).all()
                )}, 200
        return {"images": image_list_schema.dump(ImageModel.findAll_by_user(user_id))}     # noqa


# for user login
class Login(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("name",))
        user = UserModel.find_by_email(user_data.email)
        if user and user.verify_password(user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token,
                    "refresh_token": refresh_token}, 200
        current_app.logger.info(f"{user} login failed.")
        return {"msg": "Invalid Credentials."}, 401


# for user logout
class Logout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        blacklist.add(jti)
        current_app.logger.info(f"{user} logged out.")
        return {"msg": f"User[id={user_id}] has been logged out successfully"}, 200    # noqa


# for refreshing access token using acces token
class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        user = UserModel.find_by_id(current_user)
        new_token = create_access_token(identity=current_user, fresh=False)
        current_app.logger.debug(f"Acces token refreshed by {user}")
        return {"access_token": new_token}, 200
