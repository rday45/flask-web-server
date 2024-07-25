from flask import Blueprint
from init import db, bcrypt
from models.user import User

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_all_tables():
    db.create_all()
    print("All tables have been created")

@db_commands.cli.command("drop")
def drop_all_tables():
    db.drop_all()
    print("All tables have been dropped")