from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils import auth_as_admin_decorator
from better_profanity import profanity
from init import db, bcrypt
from models.user import User, user_schema, UserSchema, users_schema
from utils import check_age



auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

#users register their details.
@auth_bp.route("/register", methods=["POST"])
def register_user():
    body_data = UserSchema().load(request.get_json())

    username_is_offensive = profanity.contains_profanity(body_data.get("username"))
    younger_than_15 = check_age(body_data.get("date_of_birth")) < 15
    
    try:
        #checks if username is a swear word like 'fuck' returns an error if it is 
        if username_is_offensive:
            return {"error":"Invalid username due to offensive content. Please select a username that is not offensive."}, 403
        #checks to see if user is under the age of 15, the minimmum age of registering. returns an error if they are.
        elif younger_than_15:
            return {"error":"You need to be older than 15 to register."}, 403
        
        else:
            user = User(
                username=body_data.get("username"),
                email=body_data.get("email"),
                password=bcrypt.generate_password_hash(body_data.get("password")).decode("utf-8"),
                first_name=body_data.get("first_name"),
                last_name=body_data.get("last_name"),
                date_of_birth=body_data.get("date_of_birth"),
                phone_number=body_data.get("phone_number")
            )
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"Uh Oh. The please enter a value for the field {err.orig.diag.column_name}"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            violation_detail= err.orig.diag.message_detail
            return {"error": "Uh Oh. One of the fields you've entered requires unique information", "error_detail": violation_detail}, 409


#users login using email and password       
@auth_bp.route("/login", methods=["POST"])
def login_user():
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=2))
        return {"username":user.username, "email": user.email, "token": token}
    else:
        return {"error": "Invalid email or password"}, 401

#users update their own details    
@auth_bp.route("/users", methods=["PUT", "PATCH"])
@jwt_required()
def user_update():
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    
    if user:
        
        user.username = body_data.get("username") or user.username
        user.email = body_data.get("email") or user.email
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        else:
            user.password = user.password 
        user.first_name = body_data.get("first_name") or user.first_name
        user.last_name = body_data.get("last_name") or user.last_name
        user.phone_number = body_data.get("phone_number") or user.phone_number
        db.session.commit()
        return user_schema.dump(user)
    else:
        return {"error": "User does not exist"}

#users with admin privileges can delete other users
@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User with id {user_id} deleted succesfully"}
    else:
        return {"error": f"User with id {user_id} not found"}, 404
    

@auth_bp.route("/users")
@jwt_required()
@auth_as_admin_decorator
def get_all_users():
    stmt = db.select(User).order_by(User.id.desc())
    users = db.session.scalars(stmt)
    return users_schema.dump(users)
