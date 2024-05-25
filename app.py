from db.mongodb import MongoDBConfiguration
from flask import Flask
from flask_cors import CORS
from utils.logger import logger
from dotenv import get_variables as load_env
import os


def create_app() -> Flask:
    """
    Create a new instance of Flask application with default settings and configuration settings
    
    Returns:
    
    Flask app instance
    """
    app = Flask(__name__)
    CORS(app)

    # Load configuration from .env file
    try:
        logger.info("Loading .env")
        load_env(".env")
        logger.info(".env loaded successfully")
    except Exception as e:
        logger.error(f"An unexpected error occurred when loading the specified .env file: {e}")
    
    # Set Logger config
    if not os.path.exists(os.getenv["LOG_DIR"]):
        os.makedirs(os.getenv["LOG_DIR"])
    logger.set_file_handler(os.getenv["LOG_DIR"])
    
    # Set MongoDB config
    MongoDBConfiguration.init_db(os.getenv["MONGO_URI"], os.getenv["MONGO_DB"])

    # Register the Blueprints with the app

    return app

if __name__ == "__main__":
    from waitress import serve

    serve(create_app(), host="0.0.0.0", port=5000)