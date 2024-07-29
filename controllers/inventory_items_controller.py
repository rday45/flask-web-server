from datetime import date

from flask import Blueprint, request

from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db

from models.inventory_item import InventoryItem, inventory_item_schema, inventory_items_schema
from models.character import Character
from models.user import User
from models.item import Item


inventory_items_bp = Blueprint("inventory_items", __name__, url_prefix="/<int:character_id>/inventory-items")

@inventory_items_bp.route("/")
@jwt_required()
def get_inventory_items(character_id):
    #selects inventory_items associated with a specific character
    stmt = db.select(InventoryItem).filter_by(character_id=character_id)
    inventory_items = db.session.scalars(stmt)
    #returns all those items
    return inventory_items_schema.dump(inventory_items)


@inventory_items_bp.route("/add-item/<int:item_id>", methods=["POST"])
@jwt_required()
def add_item_to_character(character_id, item_id):
    #selects character by character's id
    stmt = db.select(Character).filter_by(id=character_id)
    character = db.session.scalar(stmt)
    #selects user by user's id based on their jwt token
    stmt2 = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt2)
    #selects item by item's id
    stmt3 = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt3)
    #selects a inventory item using both the character id and item id
    stmt4 = db.Select(InventoryItem).filter_by(character_id=character_id, item_id=item_id)
    inventory_already_assigned = db.session.scalar(stmt4)
    
    #checks if the character exists
    if not character:
        return {"error":f"Character with the id {character_id} not found"}, 404
    #checkks if the item exists
    if not item:
        return {"error":f"Item with the id {item_id} not found"}, 404
    #checks if the character's id and the user's id match or if they are an admin
    if user.id != character.user_id and not user.is_admin:
        return {"error":"you are not the owner of the character or an authorised admin"}, 403
    #checks if the character has enough money
    if character.money < item.price:
        return {"message":"That item is too expensive. You do not have enough money to attain it."}
    #checks if the item is already assigned to their inventory. if so, increases quantity in inventory_item table
    if inventory_already_assigned:
        remaining_money = character.money - item.price
        character.money = remaining_money
        new_quantity = inventory_already_assigned.quantity + 1
        inventory_already_assigned.quantity = new_quantity
        db.session.commit()
        return {"message":f"purchase successful. {character.name} has received an additional {item.name}, having a total of {inventory_already_assigned.quantity}. They have {character.money} coins left"}
    
    remaining_money = character.money - item.price
    character.money = remaining_money
    #if item does not already exist in the inventory, an inventory_item is created and added to the databasae
    inventory_item = InventoryItem(
        character_id = character.id,
        item_id = item.id,
        date_aquired = date.today()
    )
    
    db.session.add(inventory_item)
    db.session.commit()
    return {"message":f"purchase successful. {character.name} has received a {item.name}. They have {character.money} coins left"}
    

@inventory_items_bp.route("/delete-item/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(character_id,item_id):
    stmt = db.select(Character).filter_by(id=character_id)
    character = db.session.scalar(stmt)
    stmt2 = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt2)
    stmt3 = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt3)
    stmt4 = db.Select(InventoryItem).filter_by(character_id=character_id, item_id=item_id)
    inventory_already_assigned = db.session.scalar(stmt4)
    
    if not character:
        return {"error":f"Character with the id {character_id} not found"}, 404
    if not item:
        return {"error":f"Item with the id {item_id} not found"}, 404
    if user.id != character.user_id and not user.is_admin:
        return {"error":"you are not the owner of the character or an authorised admin"}, 403
    if not inventory_already_assigned:
        return{"message":"character does not have that item. Cannot be removed."}
    
    db.session.delete(inventory_already_assigned)
    db.session.commit()
    
    return{"message":f"all items: {item.name} have been removed from the inventory of {character.name}"}
    


    

