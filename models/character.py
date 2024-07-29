from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And, Regexp

#variable that stores all valid vocations for the character model
VALID_VOCATIONS = ("fighter","wizard","ranger","rogue")

#character model
class Character(db.Model):
    
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    vocation = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)
    strength = db.Column(db.Integer, nullable=False, default=1)
    constitution = db.Column(db.Integer, nullable=False, default=1)
    dexterity = db.Column(db.Integer, nullable=False, default=1)
    intelligence = db.Column(db.Integer, nullable=False, default=1)
    wisdom = db.Column(db.Integer, nullable=False, default=1)
    charisma = db.Column(db.Integer, nullable=False, default=1)
    money = db.Column(db.Integer, nullable=False, default=0)
    date_of_creation = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False,)
    
    user = db.relationship("User", back_populates="characters")

class CharacterSchema(ma.Schema):
    
    user = fields.Nested('UserSchema', only=["id", "username",])
    
    name = fields.String(required=True, validate=Length(min=3), error="The minimum length for name is 3 characters.")
    
    vocation = fields.String(required=True, validate=OneOf(VALID_VOCATIONS, error="invalid vocation, please choose fighter, wizard, ranger or rogue") )


    class Meta:
        fields = ("id","name","description","vocation","level","strength","constitution","dexterity","intelligence","wisdom","charisma","money","date_of_creation","user")
        ordered = True

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)

    