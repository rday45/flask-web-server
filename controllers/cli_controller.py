from flask import Blueprint
from init import db, bcrypt
from models.user import User

db_commands = Blueprint("db", __name__)

db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables have been created")