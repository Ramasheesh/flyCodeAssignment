import sys
import os
from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from sqlalchemy import text
from core.config import Config
from core import db
from core.apis.assignments.student import student_assignments_resources
from core.apis.assignments.teacher import teacher_assignments_resources
from core.apis.assignments.principal import principal_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(student_assignments_resources, url_prefix='/student')
    app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
    app.register_blueprint(principal_resources, url_prefix='/principal')

    # Error Handlers
    @app.errorhandler(Exception)
    def handle_error(err):
        if isinstance(err, FyleError):
            return jsonify(
                error=err.__class__.__name__, message=err.message
            ), err.status_code
        elif isinstance(err, ValidationError):
            return jsonify(
                error=err.__class__.__name__, message=err.messages
            ), 400
        elif isinstance(err, IntegrityError):
            return jsonify(
                error=err.__class__.__name__, message=str(err.orig)
            ), 400
        elif isinstance(err, HTTPException):
            return jsonify(
                error=err.__class__.__name__, message=str(err)
            ), err.code

        raise err

    # Default Route
    @app.route('/')
    def ready():
        response = jsonify({
            'status': 'ready',
            'time': helpers.get_utc_now()
        })

        return response

    return app


# Initialize the Flask app
app = create_app()


def check_db_connection():
    print("Starting database connection check...")  # Debug statement
    with app.app_context():  # Ensure we're in the app context
        print("App context initialized.")  # Debug statement
        try:
            print("Attempting to execute the test query...")  # Debug statement
            result = db.session.execute(text('SELECT 1'))
            print("Query executed, checking result...")  # Debug statement
            if result.fetchone()[0] == 1:
                print("Database connection is successful.")  # Success message
            else:
                print("Database connection failed.")  # Failure message
        except Exception as e:
            print(f"Failed to connect to SQL Database: {e}")  # Error message

if __name__ == "__main__":
    check_db_connection()  # Check database connection before running the app
    app.run(debug=True)
