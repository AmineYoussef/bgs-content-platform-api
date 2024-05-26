from flask import Blueprint, jsonify, request
from pymongo import ASCENDING, DESCENDING
from db.mongodb_helpers import *
import logging
from user.user_manager import UserManager
from models.user import UserModel
from flask_jwt_extended import jwt_required

user_routes = Blueprint("users_bp", __name__)
user_Manager = UserManager()
user_logger = logging.getLogger(__name__)
user_logger.setLevel(logging.DEBUG)

@user_routes.route("/user/<string:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id: str) -> UserModel:
    try:
        user_logger.info(f"get_user called with url {request.url}")
        user = user_Manager.get_user(user_id)
        if user is None:
            user_logger.info(f"user not found")
            return jsonify({"error": "user not found"}), 404

        return user.to_json(), 200

    except ValueError as e:
        user_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        user_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@user_routes.route("/users", methods=["GET", "POST"])
@jwt_required()
def get_users() -> ListSuccessResponse:
    try:
        user_logger.info(f"get_users called with url {request.url}")
        page = max(1, int(request.args.get("page", default=1)))
        page_size = max(1, int(request.args.get("page_size", default=10)))
        sort_by: str = request.args.get("sort_by", default="title")
        sort_direction_request: str = request.args.get(
            "sort_direction", default=ASCENDING
        )
        sort_direction = DESCENDING if sort_direction_request == "DESC" else ASCENDING
        filter_obj = request.json if request.method == "POST" else {}
        response = user_Manager.get_users(
            sort_direction, sort_by, page, page_size, filter_obj
        )
        return jsonify(response), 200

    except ValueError as e:
        user_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except IndexError as e:
        user_logger.error(f"Index Error: {str(e)}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        user_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500
