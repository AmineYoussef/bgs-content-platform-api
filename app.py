from flask import Flask
from flask_cors import CORS
from auth.auth_routes import auth_routes
from user.user_routes import user_routes
from content.content_routes import content_routes
from dotenv import load_dotenv
import os, logging
from flask_jwt_extended import JWTManager

logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s - [%(funcName)s]",
    )
app_logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)
SECRET_KEY = os.environ.get("SECRET_KEY") or "secret key goes here"
app.config["JWT_SECRET_KEY"] = SECRET_KEY
jwt = JWTManager(app)

# Load configuration from .env file
try:
    app_logger.info("Loading .env")
    load_dotenv(".env")
    app_logger.info(".env loaded successfully")
except Exception as e:
    app_logger.error(
        f"An unexpected error occurred when loading the specified .env file: {e}"
    )


# Set Logger config
if not os.path.exists(os.getenv("LOG_DIR")):
    os.makedirs(os.getenv("LOG_DIR"))


# Register the Blueprints with the app
app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)
app.register_blueprint(content_routes)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
