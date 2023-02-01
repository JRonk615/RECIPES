from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models.user import User

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.posting_user = None
        

    @classmethod
    def save_recipe(cls, data):
        if not cls.validate_recipe(data):
            return False

        query = 'INSERT INTO recipes (name, description, instructions, date_made, under, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under)s, %(user_id)s) '

        results = connectToMySQL('recipes_schema').query_db(query, data)

        return results

    @classmethod
    def get_all(cls):
            query = 'SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id'

            db = connectToMySQL('recipes_schema').query_db(query)

            all_recipes = []

            for row in db:

                posting_user = User({
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"],
                    "password": row["password"]
                })
                #  - make post instance with a user object
                new_recipe = cls(row)
                new_recipe.posting_user = posting_user
                # Add post to all_posts list
                all_recipes.append(new_recipe)

            return all_recipes

    @classmethod
    def validate_recipe(cls, data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Invalid Name', 'recipe')
            is_valid = False
        if len( data['description']) <= 0:
            flash('Invalid Description', 'recipe')
            is_valid = False
        if len( data['instructions']) <= 0:
            flash('Invalid Instructions', 'recipe')
            is_valid = False
        return is_valid
    
    @classmethod
    def delete_recipe(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'

        return connectToMySQL('recipes_schema').query_db(query, data)
        

    @classmethod
    def get_by_id(cls, data):
            query = 'SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;'

            result = connectToMySQL('recipes_schema').query_db(query, data)

            result = result[0]
            this_recipe = cls(result)

            user_data ={
                    "id": result["user_id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "email": result["email"],
                    "created_at": result["users.created_at"],
                    "updated_at": result["users.updated_at"],
                    "password": result["password"]
                }
            #     #  - make post instance with a user object
            # recipe = {
            #         "id": result["id"],
            #         "name": result["name"],
            #         "description" : result["description"],
            #         "instructions" : result["instructions"],
            #         "date_made" : result["date_made"],
            #         "under" : result["under"],
            #         "created_at": result["created_at"],
            #         "updated_at": result["updated_at"],
            #         "user": user_data
            #         }
            #     # Add post to all_posts list
            # this_recipe.append( cls(result))
            this_recipe.posting_user = User(user_data)

            return this_recipe

    @classmethod
    def get_one(cls, data):
            query = 'SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;'

            db = connectToMySQL('recipes_schema').query_db(query, data)
            
            all_recipes = []

            for row in db:

                posting_user = User({
                    "id": row["user_id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"],
                    "password": row["password"]
                })
                #  - make post instance with a user object
                new_recipe = Recipe({
                    "id": row["id"],
                    "name": row["name"],
                    "description" : row["description"],
                    "instructions" : row["instructions"],
                    "date_made" : row["date_made"],
                    "under" : row["under"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                    "user": posting_user
                    })
                # Add post to all_posts list
                all_recipes.append(new_recipe)

            return all_recipes
    
    @classmethod
    def update(cls, data):
        if not cls.validate_recipe(data):
            return False

        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under = %(under)s WHERE recipes.id = %(id)s'

        return connectToMySQL('recipes_schema').query_db(query, data)

