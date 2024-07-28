from flask import Blueprint, request
from init import db
from models.item import Item, item_schema, items_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import auth_as_admin_decorator


items_bp = Blueprint("items", __name__, url_prefix="/items")

#All users can view all items
@items_bp.route("/")
def get_all_items():
    stmt = db.select(Item).order_by(Item.price.desc())
    items = db.session.scalars(stmt)
    return items_schema.dump(items)


#All users can view individual items
@items_bp.route("/<int:item_id>")
def get_single_item(item_id):
    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt)
    if item:
        return item_schema.dump(item)
    else:
        return {"error": f"item with the id number {item_id} cannot be found"}, 404
    

#Only admins can create items
@items_bp.route("/", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def create_item():
    body_data = item_schema.load(request.get_json())

    item = Item(
        name=body_data.get("name"),
        category=body_data.get("category"),
        description=body_data.get("description"),
        strength_boost=body_data.get("strength_boost"),
        constitution_boost=body_data.get("constitution_boost"),
        dexterity_boost=body_data.get("dexterity_boost"),
        persuasion_boost=body_data.get("persuasion_boost"),
        intelligence_boost=body_data.get("intelligence_boost"),
        wisdom_boost=body_data.get("wisdom_boost"),
        charisma_boost=body_data.get("charisma_boost"),
        damage=body_data.get("damage"),
        price=body_data.get("price")
    )
    
    db.session.add(item)
    db.session.commit()

    return item_schema.dump(item)

#Only admins can update items
@items_bp.route("/<int:item_id>", methods=["PUT","PATCH"])
@jwt_required()
@auth_as_admin_decorator
def update_item(item_id):
    body_data = item_schema.load(request.get_json(), partial=True)
    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt)
    if item:
        item.name = body_data.get("name") or item.name
        item.category = body_data.get("category") or item.category
        item.description = body_data.get("description") or item.description
        item.strength_boost = body_data.get("strength_boost") or item.strength_boost
        item.constitution_boost = body_data.get("constitution_boost") or item.constitution_boost
        item.dexterity_boost = body_data.get("dexterity_boost") or item.dexterity_boost
        item.persuasion_boost = body_data.get("persuasion_boost") or item.persuasion_boost
        item.intelligence_boost = body_data.get("intelligence_boost") or item.intelligence_boost
        item.wisdom_boost = body_data.get("wisdom_boost") or item.wisdom_boost
        item.charisma_boost = body_data.get("charisma_boost") or item.charisma_boost
        item.damage = body_data.get("damage") or item.damage
        item.price = body_data.get("price") or item.price

        db.session.add(item)
        db.session.commit()
        return item_schema.dump(item)

    else:
        return {"error": f"item with the id number {item_id} cannot be found"}, 404
    
#Only admin can delete items
@items_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_item(item_id):
    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt)
    if item:
        db.session.delete(item)
        db.session.commit()
        return {"message":f"item with id {item_id} deleted successfully"}
    else:
        return {"error": f"item with id number {item_id} cannot be found"}, 404