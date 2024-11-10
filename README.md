# Role Playing Game Character and Item Manager

Many people play table top games role playing games like dungeons and dragons, estimates show that dungeons and dragon's alone has approximately 13.7 active players. When people play these games they may have to track information about their various characters including their level, statistics and equipment on paper. This project allows players to create register and create a variety of characters and purchase items for them so long as their characters have enough money. 

An admin user that functions as a dungeon master and oversees the game can level up the characters of players and change their statistics, create items in the world, and assign players gold based on events that may occur during or after a tabletop session. It is important to note that this project is not a game, it is a tool that can help be used to manage a game. Furthermore, while it is loosely based on Dungeons and Dragons (such as some of the character vocations), it does not replicate it completely and can be used for any general fantasy game.

## Initial app setup

To use this app enter the directory called 'src' or create clone of the repository by entering the following in your terminal:

```BASH
git clone https://github.com/rday45/flask-web-server.git
```
Make sure you have navigated into the directoy and create a virtual environment and activate it:

```BASH
python3 -m venv .venv
source .venv/bin/activate
```
Install the required packages with the following command:

 ```BASH
pip3 install -r requirements.txt
```

Enter PostgreSQL and create a database called rpg_db.

```BASH
CREATE DATABASE rpg_db;

```

Create a new user and set a password:
for example, you could create a user called rpg_dev with the password 123456.

```BASH
CREATE USER your_username WITH PASSWORD 'your_password';
```

Grant all privileges to your user.

```BASH
GRANT ALL PRIVILEGES ON DATABASE rpg_db to your_username;
```

Enter the database rpg_db and grant all on schema.
```BASH
\c rpg_db
GRANT ALL ON SCHEMA public TO your_username;
```

In the directory called src, create an .env file and enter the following into it:

```python
DATABASE_URL= postgresql+psycopg2://username:password@localhost/rpg_db
JWT_SECRET_KEY= "SecretKeyOfYourChoice"
```
initialise the database:

```BASH
flask db create
flask db seed
```
run the app:
```BASH
flask run
```

## Testing the app

You can test the app using Insomnia. The endpoints provided use the standard IP address for local host 127.0.0.1 
if yours is different, please make sure to adjust the endpoints.

### 1. Register user

http://127.0.0.1:5000/auth/register  

Method = POST

This endpoint registers a new user and adds their details to the database. All fields are required and admin status is set to false as default. 

Sample data that you can use:

```JSON
{
	"username":"new_user",
	"email":"new_email@fakemail.com",
	"password":"newpassword1",
	"first_name":"First",
	"last_name":"User",
	"date_of_birth":"2000-7-7",
	"phone_number":"0123456789"
}
```

If successful, the user information will entered into the database and sent back:

```JSON
{
	"id": 5,
	"username": "new_user",
	"email": "new_email@fakemail.com",
	"first_name": "First",
	"last_name": "User",
	"date_of_birth": "2000-07-07",
	"phone_number": "0123456789",
	"is_admin": false,
	"characters": []
}
```
If unsuccessful, for example, if a field is missing, you will receive an error message:

```JSON
{
	"error": {
		"username": [
			"Missing data for required field."
		]
	}
}
```

### 2. User login

http://127.0.0.1:5000/auth/login

Method = POST

This endpoint allows users to login and receive a JWT token. Please use the token you receive for other functions of the app that require authentication:

```JSON

Sample data for an admin user you can use:

```JSON
{
	"email":"admin@fakemail.com",
	"password":"adminpassword"
}
```

If successful you will receive some user details and the JSON token. For example,:

```JSON
{
	"username": "admin1",
	"email": "admin@fakemail.com",
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMjE1NTk0NiwianRpIjoiNTc1ZTk0YzMtNDJiMi00MDg5LWE4NDgtZTNhMzlhMDk1MTcyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3MjIxNTU5NDYsImNzcmYiOiIyZjU0ZDc0Yi0yOTk0LTQ3MTYtOWJhYy02YmM4ODk4ZTU4ZTQiLCJleHAiOjE3MjIzMjg3NDZ9.mcZb4Zu9qWn6QVcjC9c8uDm__lIGC0tdaClEzIA6HJE"
}
```

If unsuccessful, for example incorrect username or email, you will receive the following error:
```BASH
{
	"error": "Invalid email or password"
}
```

### Get all users

http://127.0.0.1:5000/auth/users

Method = GET

This get method requires the user to have the JSON web token of an admin as a 'bearer token.' 

If successful it will display all the user details in the database with the exception of their password.

If the user is an admin, they will receive details for all the users and some basic details of their characters:

```JSON
[
	{
		"id": 5,
		"username": "new_user",
		"email": "new_email@fakemail.com",
		"first_name": "First",
		"last_name": "User",
		"date_of_birth": "2000-07-07",
		"phone_number": "0123456789",
		"is_admin": false,
		"characters": []
	},
	{
		"id": 4,
		"username": "admin1",
		"email": "admin@fakemail.com",
		"first_name": "Timmy",
		"last_name": "Turner",
		"date_of_birth": "1986-02-12",
		"phone_number": "00000000000",
		"is_admin": true,
		"characters": []
	},
	{
		"id": 3,
		"username": "user3",
		"email": "sample_email_3@fakemail.com",
		"first_name": "Daniel",
		"last_name": "Lo",
		"date_of_birth": "1990-02-15",
		"phone_number": "1234512345",
		"is_admin": false,
		"characters": [
			{
				"id": 5,
				"name": "Danny the Wild",
				"vocation": "ranger",
				"level": 2
			},
			{
				"id": 6,
				"name": "Simple Pete",
				"vocation": "fighter",
				"level": 2
			}
		]
	},
	{
		"id": 2,
		"username": "user2",
		"email": "sample_email_2@fakemail.com",
		"first_name": "Stuart",
		"last_name": "Armitage",
		"date_of_birth": "1995-05-15",
		"phone_number": "1212112121",
		"is_admin": false,
		"characters": [
			{
				"id": 3,
				"name": "Shadow",
				"vocation": "rogue",
				"level": 3
			},
			{
				"id": 4,
				"name": "Legolas",
				"vocation": "ranger",
				"level": 3
			}
		]
	},
	{
		"id": 1,
		"username": "user1",
		"email": "sample_email_1@fakemail.com",
		"first_name": "David",
		"last_name": "Smith",
		"date_of_birth": "1995-03-18",
		"phone_number": "1234512345",
		"is_admin": false,
		"characters": [
			{
				"id": 1,
				"name": "Sir Boris",
				"vocation": "fighter",
				"level": 5
			},
			{
				"id": 2,
				"name": "Merlin",
				"vocation": "wizard",
				"level": 1
			}
		]
	}
]
```

If the user is not an admin, they will receive the following error message:

```JSON
{
	"error": "Unauthorised action. Admin privileges required."
}
```

### Update your own user details

http://127.0.0.1:5000/auth/users

Method = PUT OR PATCH

This endpoint allows a user to update their own details. note, even an admin currently cannot update another users details, they can only update their own. You can choose to send only the field you would like to update. this sample uses details for the sample user 1 which has already been seeded into the database through the CLI commands:

```JSON
{
	"email":"user_1_email_change@fakemail.com"
}
```

If successful you will receive all the updated user details, excluding the user password:

```JSON
{
	"id": 1,
	"username": "user1",
	"email": "user_1_email_change@fakemail.com",
	"first_name": "David",
	"last_name": "Smith",
	"date_of_birth": "1995-03-18",
	"phone_number": "1234512345",
	"is_admin": false,
	"characters": [
		{
			"id": 1,
			"name": "Sir Boris",
			"vocation": "fighter",
			"level": 5
		},
		{
			"id": 2,
			"name": "Merlin",
			"vocation": "wizard",
			"level": 1
		}
	]
}
```

If unsuccessful, for example you do not send the right data type associated with a field, you will receive the following error message:

```BASH
{
	"error": {
		"email": [
			"Not a valid string."
		]
	}
}
```

### Delete specific user

http://127.0.0.1:5000/auth/users/<int:id>

Method = DELETE

This endpoint will allow you to delete a user with the id specified at the end of the url. replace <int:id> with the actual id value. A user must be an authorised admin user to delete a specific user.

If successful, in this example user with the id 2 is deleted, you will receive the following response:

```JSON 
{
	"message": "User with id 2 deleted succesfully"
}
```

If unsuccesful due not being authorised, you will receive the following response:

```BASH
{
	"error": "Unauthorised action. Admin privileges required."
}
```

### View all characters and their items


http://127.0.0.1:5000/characters/

Method = GET

This endpoint will allow any logged in user to view all characters and their associated user's id and username. A user must be authenticated to use this endpoint.

If successful, the following response will be sent:

```JSON
[
	{
		"id": 1,
		"name": "Sir Boris",
		"description": "A brave gallant knight who is loyal to his king.",
		"vocation": "fighter",
		"level": 5,
		"strength": 11,
		"constitution": 11,
		"dexterity": 6,
		"intelligence": 1,
		"wisdom": 1,
		"charisma": 1,
		"money": 10,
		"date_of_creation": "2024-07-29",
		"user": {
			"id": 1,
			"username": "user1"
		}
	},
	{
		"id": 2,
		"name": "Merlin",
		"description": "A powerful wizard who is loyal to his king.",
		"vocation": "wizard",
		"level": 1,
		"strength": 1,
		"constitution": 1,
		"dexterity": 1,
		"intelligence": 1,
		"wisdom": 1,
		"charisma": 1,
		"money": 0,
		"date_of_creation": "2024-07-29",
		"user": {
			"id": 1,
			"username": "user1"
		}
	},
	{
		"id": 3,
		"name": "Shadow",
		"description": "A mysterious thief.",
		"vocation": "rogue",
		"level": 3,
		"strength": 1,
		"constitution": 1,
		"dexterity": 11,
		"intelligence": 1,
		"wisdom": 1,
		"charisma": 1,
		"money": 100,
		"date_of_creation": "2024-07-29",
		"user": {
			"id": 2,
			"username": "user2"
		}
	},
	{
		"id": 4,
		"name": "Legolas",
		"description": "The world's most famous archer.",
		"vocation": "ranger",
		"level": 3,
		"strength": 1,
		"constitution": 1,
		"dexterity": 11,
		"intelligence": 1,
		"wisdom": 1,
		"charisma": 1,
		"money": 1000,
		"date_of_creation": "2024-07-29",
		"user": {
			"id": 2,
			"username": "user2"
		}
	},
	{
		"id": 5,
		"name": "Danny the Wild",
		"description": "A hunter who has lived in the woods for all his life.",
		"vocation": "ranger",
		"level": 2,
		"strength": 1,
		"constitution": 1,
		"dexterity": 6,
		"intelligence": 1,
		"wisdom": 1,
		"charisma": 1,
		"money": 20,
		"date_of_creation": "2024-07-29",
		"user": {
			"id": 3,
			"username": "user3"
		}
	},
	{
		"id": 6,
		"name": "Simple Pete",
		"description": "A simple man who likes to smash things with his fists.",
		"vocation": "fighter",
		"level": 2,
		"strength": 6,
		"constitution": 1,
		"dexterity": 1,
		"intelligence": 1,
		"wisdom": 1,
		"charisma": 1,
		"money": 100,
		"date_of_creation": "2024-07-29",
		"user": {
			"id": 3,
			"username": "user3"
		}
	}
]
```
If not authenticated, the following response will be sent:

```JSON
{
	"msg": "Missing Authorization Header"
}
```

### View specific character

http://127.0.0.1:5000/characters/<int:id>

Method = GET

This endpoint can be used to view a specific character in the database based on their id. In this example we will be viewing character with the id of 2:

If successful, you will receive the following response which includes the attributes for a character and the user id and username of their ownser:

```JSON
{
	"id": 2,
	"name": "Merlin",
	"description": "A powerful wizard who is loyal to his king.",
	"vocation": "wizard",
	"level": 1,
	"strength": 1,
	"constitution": 1,
	"dexterity": 1,
	"intelligence": 1,
	"wisdom": 1,
	"charisma": 1,
	"money": 0,
	"date_of_creation": "2024-07-29",
	"user": {
		"id": 1,
		"username": "user1"
	}
}
```

If unsuccessful due to not being authenticated, you will receive the following response:

```JSON
{
	"msg": "Missing Authorization Header"
}
```


### Create a character

http://127.0.0.1:5000/characters

Method = POST

This endpoint is used to create a new character

To create a character, the user must be authenticated and the name and vocation field must be sent with the request(description is optional and other fields are created automatically). The character will be automatically associated with the user sending the request. An example of a request you can send includes the following:

```JSON
{
	"name":"Sneaky Jack",
	"description":"he likes to sneak",
	"vocation":"rogue"
	
}
```
If successful, you will receive the following response:

```JSON
{
	"id": 8,
	"name": "Sneaky Jack",
	"description": "he likes to sneak",
	"vocation": "rogue",
	"level": 1,
	"strength": 1,
	"constitution": 1,
	"dexterity": 1,
	"intelligence": 1,
	"wisdom": 1,
	"charisma": 1,
	"money": 0,
	"date_of_creation": "2024-07-29",
	"user": {
		"id": 1,
		"username": "user1"
	}
}
```

If the request is unsucessful, for example due to the vocation being an unaccepted value, you may receive the following error:

```JSON
{
	"error": {
		"vocation": [
			"invalid vocation, please choose fighter, wizard, ranger or rogue"
		]
	}
}
```

### Update character

http://127.0.0.1:5000/characters/<int:id>

Method = PUT or PATCH

This endpoint can update a character. characters can only be updated by their users or an admin. A user can only update their name and description whereas an admin can update most character attributes. Only the fields updated need to be sent in the request.

A sample for a user updating a character's name:

```JSON
{
	"name":"Sneaky Jack Sparrow"
}
```

If successful they will receive all the details of their character:

```JSON
{
	"id": 8,
	"name": "Sneaky Jack Sparrow",
	"description": "he likes to sneak",
	"vocation": "rogue",
	"level": 1,
	"strength": 1,
	"constitution": 1,
	"dexterity": 1,
	"intelligence": 1,
	"wisdom": 1,
	"charisma": 1,
	"money": 0,
	"date_of_creation": "2024-07-29",
	"user": {
		"id": 1,
		"username": "user1"
	}
}
```

If unsuccessful, for example the character does not belong to them, they will receive the following error:

```JSON
{
	"error": "you are not the owner of the character or an authorised admin"
}
```

### Delete character 

http://127.0.0.1:5000/characters/<int:id>

Method = DELETE

This endpoint deletes a character with the id in the url. Only owners of the character and admins can delete a character.

If successful, you will receive the following:

```JSON
{
	"message": "character with the name 'Sneaky Jack Sparrow' has been deleted successful"
}
```

If unsuccessful due to not being an admin or owner, you will receive the following error:

```JSON
{
	"error": "you are not the owner of the character or an authorised admin"
}
```


### View all items 

http://127.0.0.1:5000/items

Method = GET

This endpoint can be used to view items. The user must be authenticated in and can view all items in the database. This is similar to the view characters endpoint.

### View specific item

http://127.0.0.1:5000/items/<int:id>

Method = GET

This endpoint is used to view an individual item. <int:id> should be replaced with an item id number. The user must be authenticated and can view all items in the database. This is similar to the endpoint that allows users to view a specific character.

### Create item 

http://127.0.0.1:5000/items

method = POST

This endpoint allows admins to create items. Non admin users cannot do this. All items only require a name as all other fields have a default value or accept null values. The item category must be either miscellaneous, potion, weapon, armour or key.

For example, a new item can be created by sending the following fields as an admin:
```JSON
{
	"name":"piece of paper",
	"price":"1",
	"description":"used to write things on"
}
```
A successful response should look like this:

```JSON
{
	"id": 11,
	"name": "piece of paper",
	"category": "miscellaneous",
	"description": "used to write things on",
	"strength_boost": 0,
	"constitution_boost": 0,
	"dexterity_boost": 0,
	"persuasion_boost": 0,
	"intelligence_boost": 0,
	"wisdom_boost": 0,
	"charisma_boost": 0,
	"damage": 0,
	"price": 1
}
```
If the request is unsuccessful, for example it is missing a required field like 'name'. Then the response should be the following error:

```JSON
{
	"error": {
		"name": [
			"Missing data for required field."
		]
	}
}
```


### Update item

http://127.0.0.1:5000/items/<int:id>

Method = PUT or PATCH

This endpoint allows admins to update items. <int:id> should be replaced with the items id number. Non admin users cannot do this. As of now, when updating items the value for category must only be potion, weapon, armour or key.

The following is a sample request:

```JSON
{
	"name":"Old paper"
}
```
The following is a succesful response:

```JSON
{
	"id": 11,
	"name": "Old paper",
	"category": "miscellaneous",
	"description": "used to write things on",
	"strength_boost": 0,
	"constitution_boost": 0,
	"dexterity_boost": 0,
	"persuasion_boost": 0,
	"intelligence_boost": 0,
	"wisdom_boost": 0,
	"charisma_boost": 0,
	"damage": 0,
	"price": 1
}
```

An unsuccessful request may involve trying to change the category to one that is invalid. If so, the reponse would be the following:

```JSON
{
	"error": {
		"category": [
			"invalid category, please choose potion, weapon, armour, key or miscellaneous"
		]
	}
}
```


### Delete item

http://127.0.0.1:5000/items/<int:id>

Method = DELETE

This endpoint allows admins to delete items. <int:id> should be replaced with the items id number. Non admin users cannot do this.

If successful, you may receive a response like this:

```JSON
{
	"message": "item with id 1 deleted successfully"
}
``` 
If unsuccessful, for example if item does not exist, you should receive this response:

```JSON
{
	"error": "item with id number 90 cannot be found"
}
```


### Get all inventory items of a character

http://127.0.0.1:5000/characters/<int:character_id>/inventory-items/

method = GET

This endpoint will get all inventory items of a specific character (enter their id in the url where it says int:character_id). Any user can view any character's inventory items, however, they need to be authenticated in order to do so. 

If successful, a response may look this this:

```JSON
[
	{
		"item": {
			"id": 6,
			"name": "Wooden Spoon"
		},
		"date_aquired": "2024-07-29",
		"quantity": 1
	},
	{
		"item": {
			"id": 5,
			"name": "Wooden bowl"
		},
		"date_aquired": "2024-07-29",
		"quantity": 10
	}
]
```


### Add inventory item

http://127.0.0.1:5000/characters/<int:character_id>/inventory-items/add-item/<int:item_id>

method = POST

It is important to note that this post request should not include anything in its body as the logic is completed using the values in the url. Only one item can be added at a time. 

This endpoint allows authenticated users to add an item to their own character's inventory. They cannot add the item if the character does not belong to them unless they are an admin. Furthermore, each character has a money attribute and each item has a price attribute. If the character does not have enough money, they are not allowed to add the item to their inventory. 

When the item is added to the inventory for the first time a new inventory_items instance is created, however, if the same item is added to the inventory again, then the existing inventory_item instance will update its quantity value with +1 and the character will update its money attribute with -1. 

This endpoint uses the most complicated logic. 

A successful request may look like the following:

```JSON
{
	"message": "purchase successful. Sir Boris has received a Wooden bowl. They have 9 coins left"
}
```

If the character does not have enough money, the response should look like this:

```JSON
{
	"message": "That item is too expensive. You do not have enough money to attain it."
}
```
If the item does not exist, the response should look like this:

```JSON
{
	"error": "Item with the id 90 not found"
}
```

If no character is found, the reponse should look like this:

```JSON
{
	"error": "Character with the id 80 not found"
}
```
If the character does not belong to the user, the response should look like this:

```JSON
{
	"error": "you are not the owner of the character or an authorised admin"
}
```

### delete inventory item

http://127.0.0.1:5000/characters/<int:character_id>/inventory-items/delete-item/<int:item_id>

Method = DELETE 

PLEASE NOTE THIS USES A DIFFERENT URL FROM THE PREVIOUS ENDPOINT 

This endpoint allows the user to delete an item from their inventory. In its current state, it deletes the entire inventory_item instance rather than reducing the quantity by 1. Users can only delete their own inventory item, Admins can delete any inventory item for any character.

If they are successful they will receive the following:
```JSON
{
	"message": "all items: Potion of Strength have been removed from the inventory of Sir Boris"
}
```

Note: Potion of Strength is the name of the item and Sir Boris is the name of the character. 


If the request is unsuccessful, for example, if they do not have that item in the character's inventory, they will receive the following error:

```JSON
{
	"message": "character does not have that item. Cannot be removed."
}
```



