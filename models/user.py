from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, Length, And

#user model
class User(db.Model):
    
    __tablename__= "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique =True)
    email = db.Column(db.String, nullable = False, unique =True)
    password = db.Column(db.String, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    date_of_birth = db.Column(db.Date, nullable = False)
    phone_number = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    
    characters = db.relationship("Character", back_populates="user", cascade="all, delete")


#user schema with validation - view error messages for details.
class UserSchema(ma.Schema):
    characters = fields.List(fields.Nested('CharacterSchema', only=["id","name","vocation","level"]))
    #username validation
    username = fields.String(required=True, validate=And(
        Length(min=4, error="Username must have a minimum of 4 characters"),
        Regexp("^(?=[a-zA-Z0-9._]{4,20}$)(?!.*[_.]{2})[^_.].*[^_.]$", error="invalid username. ensure string is between 4 and 20 characters long, contains only alphanumeric characters, dots, and underscores, does not start or end with a dot or underscore, and does not have consecutive dots or underscores.")
    ))
    #email validation - ensures that the string is a valid email format with non-whitespace characters before and after the “@” symbol, and a dot separating the domain name and the top-level domain.
    email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="invalid email format"))
    #password validation
    password = fields.String(required=True, validate=Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", error="Minimum eight characters and at least one letter and one number. No symbols or spaces allowed"))
    #first name validation
    first_name = fields.String(required=True, validate=And(
        Length(min=2, error="names must be more than one character"),
        Regexp("^[a-zA-Z]+$", error="name must only contain alphabetical characters")
    ))
    #last name validation
    last_name = fields.String(required=True, validate=And(
        Length(min=2, error="names must be more than one character"),
        Regexp("^[a-zA-Z]+$", error="name must only contain alphabetical characters")
    ))
    #phone number validation
    phone_number = fields.String(required=True, validate=And(
        Length(equal=10, error ="phone number has to be 10 digits"),
        Regexp("^[0-9]*$", error="You can only use digits 0-9 for phone numbers")

    ))

    class Meta:
        fields =("id","username","email","password","first_name","last_name","date_of_birth","phone_number","is_admin","characters")
        ordered = True

#Schemas exclude password to ensure confidentiality and help keep the application secure
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])