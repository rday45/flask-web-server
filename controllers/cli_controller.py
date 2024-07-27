from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.character import Character
from models.item import Item
from models.inventory_item import InventoryItem
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
    db.session.commit()
    
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
    character_1.money = 10
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
    character_2.money = 0
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
    character_3.money = 100
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
    character_4.money = 1000
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
    character_5.money = 20
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
    character_6.money = 100
    character_6.date_of_creation = date.today()
    character_6.user = sample_user_3



    all_characters = [character_1,character_2,character_3,character_4, character_5, character_6]
    
    db.session.add_all(all_characters)
    db.session.commit()

    item_1 = Item()
    item_1.name = "Potion of Strength"
    item_1.category = "potion"
    item_1.description = "A potion that will improve your strength."
    item_1.strength_boost = 5
    item_1.price = 50

    item_2 = Item()
    item_2.name = "Potion of Intelligence"
    item_2.category = "potion"
    item_2.description = "A potion that will improve your intelligence."
    item_2.intelligence_boost = 5
    item_2.price = 50

    item_3 = Item()
    item_3.name = "Potion of Persuasion"
    item_3.category = "potion"
    item_3.description = "A potion that will improve your persuasion."
    item_3.persuasion_boost = 5
    item_3.price = 50

    item_4 = Item()
    item_4.name = "Key to Demon King's Castle"
    item_4.category = "key"
    item_4.description = "This item will grant you access to the Demon King's castle."
    item_4.price = 1000

    item_5 = Item()
    item_5.name = "Wooden bowl"
    item_5.description = "A simple wooden bowl"
    item_5.price = 1

    item_6 = Item()
    item_6.name = "Wooden Spoon"
    item_6.description = "A simple wooden spoon"
    item_6.price = 1

    all_items = [item_1, item_2, item_3, item_4, item_5, item_6]
    db.session.add_all(all_items)
    db.session.commit()


    item_assignment_1 = InventoryItem()
    item_assignment_1.character_id = character_1.id
    item_assignment_1.item_id = item_1.id

    item_assignment_2 = InventoryItem()
    item_assignment_2.character_id = character_1.id
    item_assignment_2.item_id = item_6.id

    item_assignment_3 = InventoryItem()
    item_assignment_3.character_id = character_2.id
    item_assignment_3.item_id = item_2.id

    item_assignment_3 = InventoryItem()
    item_assignment_3.character_id = character_2.id
    item_assignment_3.item_id = item_3.id

    item_assignment_4 = InventoryItem()
    item_assignment_4.character_id = character_3.id
    item_assignment_4.item_id = item_4.id

    item_assignment_5 = InventoryItem()
    item_assignment_5.character_id = character_3.id
    item_assignment_5.item_id = item_3.id

    item_assignment_6 = InventoryItem()
    item_assignment_6.character_id = character_4.id
    item_assignment_6.item_id = item_3.id

    item_assignment_7 = InventoryItem()
    item_assignment_7.character_id = character_4.id
    item_assignment_7.item_id = item_2.id


    all_item_assignments = [item_assignment_1, item_assignment_2, item_assignment_3, item_assignment_4, item_assignment_5, item_assignment_6, item_assignment_7]

    db.session.add_all(all_item_assignments)
    db.session.commit()

    
    print("All tables have been seeded")






