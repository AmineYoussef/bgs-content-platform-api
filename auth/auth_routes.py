from flask import Blueprint, jsonify, request
import logging
from db.mongodb_helpers import *
from auth.auth_manager import AuthManager
from models.user import UserInputModel, UserCredentials, UserModel
from flask_jwt_extended import create_access_token

auth_routes = Blueprint("auth", __name__)
auth_manager = AuthManager()
auth_logger = logging.getLogger(__name__)
auth_logger.setLevel(logging.DEBUG)


@auth_routes.route("/register", methods=["POST"])
def register() -> ListSuccessResponse:
    try:
        auth_logger.info(f"register called with url {request.url}")
        user_input = UserInputModel(**request.json)
        username_exists = auth_manager.verify_duplicate_username(user_input.username)
        if username_exists:
            raise ValueError("Username already taken")
        email_exists = auth_manager.verify_duplicate_email(user_input.email)
        if email_exists:
            raise ValueError("Email already taken")

        user = auth_manager.register_user(user_input)
        del user.password
        return user.to_json(), 201

    except ValueError as e:
        auth_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except IndexError as e:
        auth_logger.error(f"Index Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        auth_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@auth_routes.route("/login", methods=["POST"])
def login():
    try:
        auth_logger.info(f"login called with url {request.url}")
        user_crendentials = UserCredentials(**request.json)
        user = auth_manager.login(user_crendentials.email, user_crendentials.password)
        # token lasting 24 hours
        user = UserModel(**user).to_json()
        return jsonify({"token": create_access_token(identity=user["_id"])}), 200
    except ValueError as e:
        auth_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except IndexError as e:
        auth_logger.error(f"Index Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        auth_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500
