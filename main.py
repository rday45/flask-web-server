import os
from flask import Flask
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError, DataError
from init import db, ma, bcrypt, jwt

def create_app():
    
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400
    
    @app.errorhandler(400)
    def bad_request(err):
        return {"error": err.description}, 400
    
    @app.errorhandler(401)
    def unauthenticated():
        return {"error": "You are not authenticated"}, 401
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        return {"error":err.orig.diag.message_detail}, 409
    
    @app.errorhandler(DataError)
    def handle_data_error(err):
        return {"error": "Invalid input datatype for one of the given fields"}, 400

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.character_controller import characters_bp
    app.register_blueprint(characters_bp)

    from controllers.item_controller import items_bp
    app.register_blueprint(items_bp)

    from controllers.authentication_controller import auth_bp
    app.register_blueprint(auth_bp)

    return app