from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    db = "recipes"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.under_30_min = data["under_30_min"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        if "first_name" in data:
            self.first_name = data["first_name"]
        else:
            self.first_name = None
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            all_recipes.append(cls(row))
        return all_recipes
    
    @classmethod
    def get_all_with_creators(cls):
        query = """SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            all_recipes.append(cls(row))
        return all_recipes

    @classmethod
    def create(cls, data):
        query = """INSERT INTO recipes (name, description, instructions, date_cooked, under_30_min, user_id)
            VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30_min)s, %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_one_with_user(cls, data):
        query = """SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id 
            WHERE recipes.id=%(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        row = results[0]
        one_recipe = cls(row)
        return one_recipe

    @classmethod
    def update(cls, data):
        query = """UPDATE recipes SET
            name=%(name)s,
            description=%(description)s,
            instructions=%(instructions)s,
            date_cooked=%(date_cooked)s,
            under_30_min=%(under_30_min)s
            WHERE id=%(id)s;""" 
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def destroy(cls, data):
        query = """DELETE FROM recipes WHERE id=%(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def is_valid(movie):
        is_valid = True
        
        if len(movie["name"]) < 3:
            is_valid = False
            flash("Name should have at least 3 characters")
        if len(movie["description"]) < 3:
            is_valid = False
            flash("Description should have at least 3 characters")
        if len(movie["instructions"]) < 3:
            is_valid = False
            flash("Instructions should have at least 3 characters")
        return is_valid
        
    
        