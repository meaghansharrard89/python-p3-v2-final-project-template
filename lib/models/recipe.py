from models.__init__ import CURSOR, CONN
from models.ingredient import Ingredient
from models.category import Category


class Recipe:
    all = {}

    def __init__(self, title, instructions, ingredients=None, id=None):
        self._id = id
        self._title = title
        self._instructions = instructions
        self._ingredients = (
            ingredients or []
        )  # Use an empty list if ingredients is None

    @property
    def id(self):
        return self._id

    @property
    def name(self):  # Updated property name
        return self._title

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value):
            self._title = value
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def ingredients(self):
        return self._ingredients

    @ingredients.setter
    def ingredients(self, value):
        self._ingredients = value

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS recipes"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = "INSERT INTO recipes (name, category_id) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.category.id))
        recipe_id = CURSOR.lastrowid

        for ingredient in self.ingredients:
            sql = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?, ?)"
            CURSOR.execute(sql, (recipe_id, ingredient.id))

        CONN.commit()

    def delete(self):
        sql = "DELETE FROM recipes WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def instance_from_db(cls, row):
        recipe = cls.all.get(row[0])
        if recipe:
            recipe.name = row[1]
            recipe.category = Category.find_by_id(
                row[2]
            )  # Assuming Category class has a find_by_id method
        else:
            recipe = cls(row[1], Category.find_by_id(row[2]), [])
            recipe._id = row[0]
            cls.all[recipe.id] = recipe
        return recipe

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM recipes"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, recipe_id):
        sql = "SELECT * FROM recipes WHERE id = ?"
        row = CURSOR.execute(sql, (recipe_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # Add this method to associate an ingredient with a recipe
    def associate_ingredient(self, ingredient):
        self._ingredients.append(ingredient)

    # Add this method to add an ingredient by name
    def add_ingredient(self, ingredient_name):
        ingredient = Ingredient.find_by_name(ingredient_name)
        if ingredient:
            self.associate_ingredient(ingredient)
        else:
            print(f"Ingredient '{ingredient_name}' not found.")

    @classmethod
    def find_by_title(cls, title):
        # Find a recipe by its title
        sql = """
            SELECT *
            FROM recipes
            WHERE title = ?
        """
        # Return the first table row of a Recipe object matching a title
        row = CURSOR.execute(sql, (title,)).fetchone()
        return cls.instance_from_db(row) if row else None
