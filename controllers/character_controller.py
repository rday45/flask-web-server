from datetime import date

from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.character import Character, character_schema, characters_schema
from models.user import User
from controllers.inventory_items_controller import inventory_items_bp


characters_bp = Blueprint("characters", __name__, url_prefix="/characters")
characters_bp.register_blueprint(inventory_items_bp)

#Note - all users can view all the characters in the database and the username and id of the users the characters belong to.
#route to view all characters in the database
@characters_bp.route("/")
@jwt_required()
def get_all_characters():
    stmt = db.select(Character).order_by(Character.date_of_creation.desc())
    characters = db.session.scalars(stmt)
    return characters_schema.dump(characters)

    
    #route to view a single character in the database based on character id passed through the url
@characters_bp.route("/<int:character_id>")
@jwt_required()
def get_single_character(character_id):
    stmt = db.select(Character).filter_by(id=character_id)
    character = db.session.scalar(stmt)
    if character:
        return character_schema.dump(character)
    else:
        return {"error": f"Character with the id number {character_id} cannot be found"}, 404

#route for creating a character. Each user can create characters that will be linked to them
@characters_bp.route("/", methods=["POST"])
@jwt_required()
def create_character():
    body_data = character_schema.load(request.get_json())

    character = Character(
        name=body_data.get("name"),
        description=body_data.get("description"),
        vocation=body_data.get("vocation"),
        date_of_creation=date.today(),
        user_id=get_jwt_identity()
    )

    db.session.add(character)
    db.session.commit()

    return character_schema.dump(character)

#route for updating character. User can only update their own character's name and description. Admin can update any character and most attributes of the character.
@characters_bp.route("/<int:character_id>", methods =["PUT","PATCH"])
@jwt_required()
def update_character(character_id):
    body_data = character_schema.load(request.get_json(), partial=True)
    stmt = db.select(Character).filter_by(id=character_id)
    character = db.session.scalar(stmt)
    stmt2 = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt2)
    
    if not character:
        return {"error":f"Character with the id {character_id} not found"}, 404
    if user.id != character.user_id and not user.is_admin:
        return {"error":"you are not the owner of the character or an authorised admin"}, 403
    
    #All users can change their character's name and description
    character.name = body_data.get("name") or character.name
    character.description = body_data.get("description") or character.description
    #Only admin users can change these attributes of a character
    if user.is_admin:
        character.vocation = body_data.get("vocation") or character.vocation
        character.level = body_data.get("level") or character.level
        character.strength = body_data.get("strength") or character.strength
        character.constitution = body_data.get("constitution") or character.constitution
        character.dexterity = body_data.get("dexterity") or character.dexterity
        character.intelligence = body_data.get("intelligence") or character.intelligence
        character.wisdom = body_data.get("wisdom") or character.wisdom
        character.charisma = body_data.get("charisma") or character.charisma
        character.money = body_data.get("money") or character.money
    
    db.session.commit()
    return character_schema.dump(character)


@characters_bp.route("/<int:character_id>", methods =["DELETE"])
@jwt_required()
def delete_character(character_id):
    #selects character based on the value passed through the url
    stmt = db.select(Character).filter_by(id=character_id)
    character = db.session.scalar(stmt)
    #selects user based on their jwt token
    stmt2 = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt2)
    if not character:
        return {"error":f"Character with the id {character_id} not found"}, 404
    if user.id != character.user_id and not user.is_admin:
        return {"error":"you are not the owner of the character or an authorised admin"}, 403
    db.session.delete(character)
    db.session.commit()
    return {"message":f"character with the name '{character.name}' has been deleted successful"}


    