from models.__init__ import CURSOR, CONN
from models.ingredient import Ingredient
from models.category import Category


class Recipe:
    all = {}

    def __init__(self, title, instructions, ingredients, category, id=None):
        self._id = id
        self._title = title
        self._instructions = instructions
        self._ingredients = ingredients
        self._category = category

    @property
    def id(self):
        return self._id

    @property
    def title(self):  # Updated property title
        return self._title

    @title.setter
    def title(self, value):
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

    @property
    def instructions(self):
        return self._instructions

    @instructions.setter
    def instructions(self, value):
        self._instructions = value

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                category TEXT
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
        # Convert the list of ingredients to a comma-separated string
        ingredients_str = ", ".join(str(ingredient) for ingredient in self.ingredients)

        # Save the recipe details
        sql = "INSERT INTO recipes (title, ingredients, instructions, category) VALUES (?, ?, ?, ?)"
        CURSOR.execute(
            sql,
            (
                self.title,
                ingredients_str,
                self.instructions,
                self.category.name if self.category else None,
            ),
        )
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM recipes WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def instance_from_db(cls, row):
        recipe = cls.all.get(row[0])
        if recipe:
            recipe.title = row[1]
            recipe.ingredients = row[2]
            recipe.instructions = row[3]
            recipe.category = row[4]

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
            print(f"Ingredient '{ingredient_name}' already exists.")
        else:
            self.associate_ingredient(ingredient)

    # Add this method to associate a category with a recipe

    def associate_category(self, category):
        self._categories.append(category)

    # Add this method to add a category by name
    def add_category(self, category_name):
        category = Category.find_by_name(category_name)
        if category:
            print(f"Category '{category_name}' already exists.")
        else:
            self.associate_category(category)

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
