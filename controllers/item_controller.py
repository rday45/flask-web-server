from flask import Blueprint, request
from init import db
from models.item import Item, item_schema, items_schema


items_bp = Blueprint("items", __name__, url_prefix="/items")

@items_bp.route("/")
def get_all_characters():
    stmt = db.select(Item).order_by(Item.price.desc())
    items = db.session.scalars(stmt)
    return items_schema.dump(items)


@items_bp.route("/<int:item_id>")
def get_single_character(item_id):
    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt)
    if item:
        return item_schema.dump(item)
    else:
        return {"error": f"item with the id number {item_id} cannot be found"}, 404