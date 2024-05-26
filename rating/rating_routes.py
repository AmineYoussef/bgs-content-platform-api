from flask import Blueprint, jsonify, request
from pymongo import ASCENDING, DESCENDING
from db.mongodb_helpers import *
import logging
from rating.rating_controller import RatingController
from models.rating import *
from flask_jwt_extended import jwt_required, get_jwt_identity

rating_routes = Blueprint("ratings_bp", __name__)
rating_controller = RatingController()
rating_logger = logging.getLogger(__name__)
rating_logger.setLevel(logging.DEBUG)


@rating_routes.route("/rating/<string:rating_id>", methods=["GET"])
def get_rating(rating_id: str) -> RatingModel:
    try:
        rating_logger.info(f"get_rating called with url {request.url}")
        rating = rating_controller.get_rating(rating_id)
        if rating is None:
            rating_logger.info(f"rating not found")
            return jsonify({"error": "rating not found"}), 404

        return rating.to_json(), 200

    except ValueError as e:
        rating_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        rating_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@rating_routes.route("/ratings", methods=["GET"])
@jwt_required()
def get_user_ratings() -> ListSuccessResponse:
    try:
        rating_logger.info(f"get_rating called with url {request.url}")
        page = max(1, int(request.args.get("page", default=1)))
        page_size = max(1, int(request.args.get("page_size", default=10)))
        sort_by: str = request.args.get("sort_by", default="title")
        sort_direction_request: str = request.args.get(
            "sort_direction", default=ASCENDING
        )
        sort_direction = DESCENDING if sort_direction_request == "DESC" else ASCENDING
        current_user = get_jwt_identity()
        filter_obj = {"user_id": current_user}
        response = rating_controller.get_ratings(
            sort_direction, sort_by, page, page_size, filter_obj
        )
        return jsonify(response), 200

    except ValueError as e:
        rating_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except IndexError as e:
        rating_logger.error(f"Index Error: {str(e)}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        rating_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@rating_routes.route("/content/<string:content_id>/ratings", methods=["GET"])
@jwt_required()
def get_content_ratings(content_id: str) -> ListSuccessResponse:
    try:
        rating_logger.info(f"get_rating called with url {request.url}")
        page = max(1, int(request.args.get("page", default=1)))
        page_size = max(1, int(request.args.get("page_size", default=10)))
        sort_by: str = request.args.get("sort_by", default="title")
        sort_direction_request: str = request.args.get(
            "sort_direction", default=ASCENDING
        )
        sort_direction = DESCENDING if sort_direction_request == "DESC" else ASCENDING
        filter_obj = {"content_id": content_id}
        response = rating_controller.get_ratings(
            sort_direction, sort_by, page, page_size, filter_obj
        )
        return jsonify(response), 200

    except ValueError as e:
        rating_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except IndexError as e:
        rating_logger.error(f"Index Error: {str(e)}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        rating_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@rating_routes.route("/content/<string:content_id>/rate", methods=["POST"])
@jwt_required()
def add_rating(content_id: str) -> RatingModel:
    try:
        rating_logger.info(f"add_rating called with url {request.url}")
        current_user = get_jwt_identity()
        request.json["user_id"] = current_user
        request.json["content_id"] = content_id
        rating_input = RatingInputModel(**request.json)

        rating = rating_controller.add_rating(rating_input)
        return rating.to_json(), 201

    except ValueError as e:
        rating_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except IndexError as e:
        rating_logger.error(f"Index Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        rating_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@rating_routes.route("/rating/<string:rating_id>", methods=["PUT"])
@jwt_required()
def update_rating(rating_id: str) -> Dict[str, Any]:
    try:
        rating_logger.info(f"rating called with url {request.url}")
        existing_rating = rating_controller.get_rating(rating_id)

        if request.json == {}:
            rating_logger.info(f"Empty request body")
            return jsonify({"error": "Empty request body"}), 400
        update_data = PartialRatingModel(**request.json)

        if existing_rating is None:
            rating_logger.info(f"Rating not found")
            return jsonify({"error": "Rating not found"}), 404
        updated_rating = rating_controller.update_rating(
            update_data.dict(exclude_unset=True), rating_id
        )

        return updated_rating.to_json(), 200

    except ValueError as e:
        rating_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        rating_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@rating_routes.route("/rating/<string:rating_id>", methods=["DELETE"])
@jwt_required()
def delete_rating(rating_id: str):
    try:
        rating_logger.info(f"delete_rating called with url {request.url}")
        existing_rating = rating_controller.get_rating(rating_id)

        if existing_rating is None:
            rating_logger.info(f"Rating not found")
            return jsonify({"error": "Rating not found"}), 404

        rating_controller.delete_rating(rating_id)

        return jsonify({"message": "Rating deleted successfully"}), 200
    except Exception as e:
        rating_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500
