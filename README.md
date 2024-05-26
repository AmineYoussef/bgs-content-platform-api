# Flask-RESTful API project template

This is a basic backend API for managing content with JWT Auth. It uses Flask and MongoDB as a DB

Project structure:
The project adapts a modular architecture

```
.
├── README.md
├── app.py
├── setup.py
├── docs
├── auth
│   ├── __init__.py
│   └── auth_manager.py
│   └── auth_routes.py
├── content
│   ├── __init__.py
│   └── content_manager.py
│   └── content_routes.py
├── db
│   ├── __init__.py
│   └── mongodb_connection.py
│   └── mongodb_helpers.py
├── auth
│   ├── __init__.py
│   └── content.py
│   └── py_object_id.py
│   └── rating.py
│   └── response.py
│   └── user.py
├── rating
│   ├── __init__.py
│   └── rating_manager.py
│   └── rating_routes.py
├── user
│   ├── __init__.py
│   └── user_manager.py
│   └── user_routes.py
```

## Environment

add a .env file with the following structure

```
MONGO_URI = "your_mongodb_connection_string"
MONGO_DB = "your_database_name"
SECRET_KEY = "secret key with SHA256"
DEBUG = True
```

### Prerequisites
Ensure you have the following installed:
- Python 3.10.x
- pip

### Installation

1. Clone the repository

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    ```

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

3. Install the package:
    ```bash
    pip install .
    ```

4. Run the following command to start the application:
    ```bash
    flask --app app run --debug --host=0.0.0.0 --port=5000
    ```

## Documentation

Using Postman, import the collections and environment variables found inside the docs folder
