from flask import Blueprint, request
from init import db
from sqlalchemy.exc import ProgrammingError
from psycopg2 import errorcodes
from models.character import Character, character_schema, characters_schema
from controllers.inventory_items_controller import inventory_items_bp


characters_bp = Blueprint("characters", __name__, url_prefix="/characters")
characters_bp.register_blueprint(inventory_items_bp)

#Note - all users can view all the characters in the database and the username and id of the users the characters belong to.
#route to view all characters in the database
@characters_bp.route("/")
def get_all_characters():
    stmt = db.select(Character).order_by(Character.date_of_creation.desc())
    characters = db.session.scalars(stmt)
    return characters_schema.dump(characters)



    

#route to view a single character in the database based on character id passed through the url
@characters_bp.route("/<int:character_id>")
def get_single_character(character_id):
    stmt = db.select(Character).filter_by(id=character_id)
    character = db.session.scalar(stmt)
    if character:
        return character_schema.dump(character)
    else:
        return {"error": f"Character with the id number {character_id} cannot be found"}, 404
