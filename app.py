from flask import Flask
from flask_cors import CORS
from auth.auth_routes import auth_routes
from user.user_routes import user_routes
from content.content_routes import content_routes
from rating.rating_routes import rating_routes
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
import os, logging
from flask_jwt_extended import (
    JWTManager,
    get_jwt,
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s - [%(funcName)s]",
)
app_logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)

# Load configuration from .env file
try:
    app_logger.info("Loading .env")
    load_dotenv(".env")
    app_logger.info(".env loaded successfully")
except Exception as e:
    app_logger.error(
        f"An unexpected error occurred when loading the specified .env file: {e}"
    )

# Load JWT configuration
SECRET_KEY = os.environ.get("SECRET_KEY") or "secret key goes here"
app.config["JWT_COOKIE_SECURE"] = False if os.getenv("DEBUG") == "True" else True
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

@app.after_request
def refresh_expiring_jwts(response):
    try:
        app_logger.info("Refreshing expiring jwt token")
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


# Set Logger config
if not os.path.exists(os.getenv("LOG_DIR")):
    os.makedirs(os.getenv("LOG_DIR"))


# Register the Blueprints with the app
app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)
app.register_blueprint(content_routes)
app.register_blueprint(rating_routes)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
