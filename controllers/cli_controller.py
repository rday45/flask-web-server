from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.character import Character
from datetime import date

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_all_tables():
    db.create_all()
    print("All tables have been created")

@db_commands.cli.command("drop")
def drop_all_tables():
    db.drop_all()
    print("All tables have been dropped")

@db_commands.cli.command("seed")
def seed_all_tables():
    
    sample_user_1 = User()
    sample_user_1.email = "sample_email_1@fakemail.com"
    sample_user_1.username = "user1"
    sample_user_1.password = bcrypt.generate_password_hash("password1").decode("utf-8")
    sample_user_1.first_name = "David"
    sample_user_1.last_name = "Smith"
    sample_user_1.phone_number = "1234512345"
    sample_user_1.date_of_birth = "1995-3-18"
    sample_user_1.is_admin = False

    sample_user_2 = User()
    sample_user_2.email = "sample_email_2@fakemail.com"
    sample_user_2.username = "user2"
    sample_user_2.password = bcrypt.generate_password_hash("password2").decode("utf-8")
    sample_user_2.first_name = "Stuart"
    sample_user_2.last_name = "Armitage"
    sample_user_2.phone_number = "1212112121"
    sample_user_2.date_of_birth = "1995-5-15"
    sample_user_2.is_admin = False

    sample_user_3 = User()
    sample_user_3.email = "sample_email_3@fakemail.com"
    sample_user_3.username = "user3"
    sample_user_3.password = bcrypt.generate_password_hash("password3").decode("utf-8")
    sample_user_3.first_name = "Daniel"
    sample_user_3.last_name = "Lo"
    sample_user_3.phone_number = "1234512345"
    sample_user_3.date_of_birth = "1990-2-15"
    sample_user_3.is_admin = False

    admin_user = User()
    admin_user.email = "admin@fakemail.com"
    admin_user.username = "admin1"
    admin_user.password = bcrypt.generate_password_hash("adminpassword").decode("utf-8")
    admin_user.first_name = "Timmy"
    admin_user.last_name = "Turner"
    admin_user.phone_number = "00000000000"
    admin_user.date_of_birth = "1986-2-12"
    admin_user.is_admin = True

    all_users = [sample_user_1,sample_user_2,sample_user_3,admin_user]
    
    db.session.add_all(all_users)
    
    character_1 = Character()
    character_1.name = "Sir Boris"
    character_1.description = "A brave gallant knight who is loyal to his king."
    character_1.vocation = "fighter"
    character_1.level = 5
    character_1.strength = 11
    character_1.constitution = 11
    character_1.dexterity = 6
    character_1.intelligence = 1
    character_1.wisdom = 1
    character_1.charisma = 1
    character_1.power_up_points = 0
    character_1.date_of_creation = date.today()
    character_1.user = sample_user_1

    character_2 = Character()
    character_2.name = "Merlin"
    character_2.description = "A powerful wizard who is loyal to his king."
    character_2.vocation = "wizard"
    character_2.level = 1
    character_2.strength = 1
    character_2.constitution = 1
    character_2.dexterity = 1
    character_2.intelligence = 1
    character_2.wisdom = 1
    character_2.charisma = 1
    character_2.power_up_points = 0
    character_2.date_of_creation = date.today()
    character_2.user = sample_user_1

    character_3 = Character()
    character_3.name = "Shadow"
    character_3.description = "A mysterious thief."
    character_3.vocation = "rogue"
    character_3.level = 3
    character_3.strength = 1
    character_3.constitution = 1
    character_3.dexterity = 11
    character_3.intelligence = 1
    character_3.wisdom = 1
    character_3.charisma = 1
    character_3.power_up_points = 0
    character_3.date_of_creation = date.today()
    character_3.user = sample_user_2

    character_4 = Character()
    character_4.name = "Legolas"
    character_4.description = "The world's most famous archer."
    character_4.vocation = "ranger"
    character_4.level = 3
    character_4.strength = 1
    character_4.constitution = 1
    character_4.dexterity = 11
    character_4.intelligence = 1
    character_4.wisdom = 1
    character_4.charisma = 1
    character_4.power_up_points = 0
    character_4.date_of_creation = date.today()
    character_4.user = sample_user_2

    character_5 = Character()
    character_5.name = "Danny the Wild"
    character_5.description = "A hunter who has lived in the woods for all his life."
    character_5.vocation = "ranger"
    character_5.level = 2
    character_5.strength = 1
    character_5.constitution = 1
    character_5.dexterity = 6
    character_5.intelligence = 1
    character_5.wisdom = 1
    character_5.charisma = 1
    character_5.power_up_points = 0
    character_5.date_of_creation = date.today()
    character_5.user = sample_user_3

    character_6 = Character()
    character_6.name = "Simple Pete"
    character_6.description = "A simple man who likes to smash things with his fists."
    character_6.vocation = "fighter"
    character_6.level = 2
    character_6.strength = 6
    character_6.constitution = 1
    character_6.dexterity = 1
    character_6.intelligence = 1
    character_6.wisdom = 1
    character_6.charisma = 1
    character_6.power_up_points = 0
    character_6.date_of_creation = date.today()
    character_6.user = sample_user_3



    all_characters = [character_1,character_2,character_3,character_4, character_5, character_6]
    
    db.session.add_all(all_characters)
    db.session.commit()

    




    
    
    
    db.session.commit()
    print("All tables have been seeded")






