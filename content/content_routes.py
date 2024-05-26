from flask import Blueprint, jsonify, request
from pymongo import ASCENDING, DESCENDING
from db.mongodb_helpers import *
import logging
from content.content_manager import ContentManager
from models.content import *
from flask_jwt_extended import jwt_required, get_jwt_identity

content_routes = Blueprint("content_bp", __name__)
content_manager = ContentManager()
content_logger = logging.getLogger(__name__)
content_logger.setLevel(logging.DEBUG)


@content_routes.route("/content/<string:content_id>", methods=["GET"])
def get_content(content_id: str) -> ContentModel:
    try:
        content_logger.info(f"get_content called with url {request.url}")
        content = content_manager.get_content(content_id)
        if content is None:
            content_logger.info(f"content not found")
            return jsonify({"error": "content not found"}), 404

        return content.to_json(), 200

    except ValueError as e:
        content_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        content_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@content_routes.route("/content", methods=["GET", "POST"])
def get_contents() -> ListSuccessResponse:
    try:
        content_logger.info(f"get_content called with url {request.url}")
        page = max(1, int(request.args.get("page", default=1)))
        page_size = max(1, int(request.args.get("page_size", default=10)))
        sort_by: str = request.args.get("sort_by", default="title")
        sort_direction_request: str = request.args.get(
            "sort_direction", default=ASCENDING
        )
        sort_direction = DESCENDING if sort_direction_request == "DESC" else ASCENDING
        filter_obj = (
            ContentFilterModel(**request.json) if request.method == "POST" else {}
        )
        response = content_manager.get_content_list(
            sort_direction, sort_by, page, page_size, filter_obj
        )
        return jsonify(response), 200

    except ValueError as e:
        content_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        content_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@content_routes.route("/content/add", methods=["POST"])
@jwt_required()
def add_content() -> ContentModel:
    try:
        content_logger.info(f"add_content called with url {request.url}")
        current_user = get_jwt_identity()
        request.json["created_by"] = current_user
        content_logger.debug(request.json)
        content_input = ContentInputModel(**request.json)
        content = content_manager.add_content(content_input)
        return content.to_json(), 201
    except ValueError as e:
        content_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        content_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@content_routes.route("/content/<string:content_id>", methods=["PUT"])
@jwt_required()
def update_content(content_id: str) -> Dict[str, Any]:
    try:
        content_logger.info(f"content called with url {request.url}")
        existing_content = content_manager.get_content(content_id)
        current_user = get_jwt_identity()
        if existing_content is None:
            content_logger.info(f"Content not found")
            return jsonify({"error": "Content not found"}), 404
        
        if existing_content.created_by != current_user:
            return (
                jsonify(
                    {
                        "error": "You are not allowed to edit content that you did not create"
                    }
                ),
                403,
            )

        if request.json == {}:
            content_logger.info(f"Empty request body")
            return jsonify({"error": "Empty request body"}), 400
        update_data = PartialContentModel(**request.json)

        if existing_content is None:
            content_logger.info(f"Content not found")
            return jsonify({"error": "Content not found"}), 404
        updated_content = content_manager.update_content(
            update_data.dict(exclude_unset=True), content_id
        )

        return updated_content.to_json(), 200

    except ValueError as e:
        content_logger.error(f"Value Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        content_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@content_routes.route("/content/<string:content_id>", methods=["DELETE"])
@jwt_required()
def delete_content(content_id: str):
    try:
        content_logger.info(f"delete_content called with url {request.url}")
        existing_content = content_manager.get_content(content_id)
        current_user = get_jwt_identity()

        if existing_content is None:
            content_logger.info(f"Content not found")
            return jsonify({"error": "Content not found"}), 404

        if existing_content.created_by != current_user:
            return (
                jsonify(
                    {
                        "error": "You are not allowed to delete content that you did not create"
                    }
                ),
                403,
            )
        content_manager.delete_content(content_id)
        return jsonify({"message": "Content deleted successfully"}), 200
    except Exception as e:
        content_logger.error(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500
