from init import db, ma
from marshmallow import fields
from datetime import date

# model that serves as a joining table for characters and items
class InventoryItem(db.Model):
    __tablename__ ="inventory_items"
    
    id = db.Column(db.Integer, primary_key=True)
    #foreign keys that connect to the characters model and items model. Ensures that instances of this model are deleted when their associated character or item is deleted.
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    date_aquired = db.Column(db.Date, nullable=False, default=date.today())
    quantity = db.Column(db.Integer, nullable=False, default=1)

    item = db.relationship("Item")


class InventoryItemSchema(ma.Schema):
    
    item = fields.Nested('ItemSchema', only=["id","name"])
    
    class Meta:
        fields = ("item","id","character_id","item_id","date_aquired","quantity",)
        ordered = True

inventory_item_schema = InventoryItemSchema(exclude=["id","character_id","item_id"])
inventory_items_schema = InventoryItemSchema(exclude=["id","character_id","item_id"], many=True)


