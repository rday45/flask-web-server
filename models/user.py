from init import db, ma

class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique =True)
    email = db.Column(db.String, nullable = False, unique =True)
    password = db.Column(db.String, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    #possibly add age verification. You have to be over 15 years of age to register
    date_of_birth = db.Column(db.Date, nullable = False)
    phone_number = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
    class Meta:
        fields =("id","username","email","password","first_name","last_name","date_of_birth","phone_number","is_admin")

#maybe include some user schemas that have more privacy for when other players want to each other's information
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])