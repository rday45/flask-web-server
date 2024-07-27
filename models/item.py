from init import db,ma
from marshmallow import fields

class Item(db.Model):
    
    __tablename__="items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False, default="miscellaneous")
    description = db.Column(db.String)
    strength_boost = db.Column(db.Integer, nullable=False, default=0)
    constitution_boost = db.Column(db.Integer, nullable=False, default=0)
    dexterity_boost = db.Column(db.Integer, nullable=False, default=0)
    persuasion_boost = db.Column(db.Integer, nullable=False, default=0)
    intelligence_boost = db.Column(db.Integer, nullable=False, default=0)
    wisdom_boost = db.Column(db.Integer, nullable=False, default=0)
    charisma_boost = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Integer, nullable=False, default=0)


class ItemSchema(ma.Schema):
    class Meta:
        fields = ("id","name","category","description","strength_boost","constitution_boost","dexterity_boost","persuasion_boost","intelligence_boost","wisdom_boost","charisma_boost","price")
        ordered = True

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

