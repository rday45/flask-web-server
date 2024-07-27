from flask import Blueprint, request
from init import db
from models.inventory_item import InventoryItem, inventory_item_schema, inventory_items_schema

inventory_items_bp = Blueprint("inventory_items", __name__, url_prefix="/<int:character_id>/inventory-items")

@inventory_items_bp.route("/")
def get_inventory_items(character_id):
    
    stmt = db.select(InventoryItem).filter_by(character_id=character_id)
    inventory_items = db.session.scalars(stmt)
    return inventory_items_schema.dump(inventory_items)
 
    