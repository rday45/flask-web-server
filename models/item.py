from init import db,ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf


#variable that stores the only possible categories for an instance of the item model
VALID_ITEMS = ("potion","weapon","armour","key","miscellaneous")


#item model
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
    damage = db.Column(db.Integer, nullable = False, default =0)
    price = db.Column(db.Integer, nullable=False, default=0)


#item schema with validation - view error messages for details
class ItemSchema(ma.Schema):
    #validates item name
    name = fields.String(required=True, validate=And(
        Length(min=3, error="The minimum length for name is 3 characters."),
        Regexp("^(?! )[A-Za-z0-9 ]*(?<! )$", error="name must only contain numbers and letters. Spaces can only exist between words")
    ))
    #validates item description
    description = fields.String(required=True, validate=And(
        Length(min=3, error="The minimum length for description is 3 characters."),
        Regexp("^(?! )[A-Za-z0-9 ]*(?<! )$", error="description must only contain numbers and letters. Spaces can only exist between words")
    ))
    #validates item category
    category = fields.String(validate=OneOf(VALID_ITEMS, error="invalid category, please choose potion, weapon, armour, key or miscellaneous") )

    class Meta:
        fields = ("id","name","category","description","strength_boost","constitution_boost","dexterity_boost","persuasion_boost","intelligence_boost","wisdom_boost","charisma_boost","damage","price",)
        ordered = True


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

