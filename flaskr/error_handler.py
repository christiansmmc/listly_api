from flask import jsonify
from marshmallow import ValidationError

from flaskr.schemas.error import ErrorSchema


def configure_error_handlers(app):
    @app.errorhandler(400)
    def bad_request_error(error):
        if isinstance(error.description, ValidationError):
            error_schema = ErrorSchema()
            response = error_schema.dump({
                "status": 400,
                "message": "Invalid request data",
                "errors": error.description.messages
            })
        else:
            response = {
                "status": "400",
                "message": str(error.description) if error.description else "Bad Request"
            }

        return jsonify(response), 400

    @app.errorhandler(404)
    def not_found_error(error):
        error_schema = ErrorSchema()
        response = error_schema.dump({
            "status": "404",
            "message": str(error.description) if error.description else "The requested resource was not found."
        })

        return jsonify(response), 404

    @app.errorhandler(500)
    def internal_server_error():
        error_schema = ErrorSchema()
        response = error_schema.dump({
            "status": "500",
            "message": "An unexpected error occurred. Please try again later."
        })

        return jsonify(response), 500
