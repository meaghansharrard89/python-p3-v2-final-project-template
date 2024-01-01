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
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and len(title):
            self._title = title
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def ingredients(self):
        return self._ingredients

    @ingredients.setter
    def ingredients(self, ingredients):
        self._ingredients = ingredients

    @property
    def instructions(self):
        return self._instructions

    @instructions.setter
    def instructions(self, instructions):
        self._instructions = instructions

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
        category_name = self.category if self.category else None
        sql = "INSERT INTO recipes (title, ingredients, instructions, category) VALUES (?, ?, ?, ?)"
        CURSOR.execute(
            sql,
            (
                self.title,
                ingredients_str,
                self.instructions,
                category_name,
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
            recipe.category = row[
                4
            ]  # Directly assign the category name from the database

        else:
            # Split the ingredients string into a list
            ingredients = (
                [ingredient.strip() for ingredient in row[2].split(",")]
                if row[2]
                else []
            )
            category_name = row[4]
            recipe = cls(row[1], row[3], ingredients, None)
            recipe._id = row[0]
            recipe.category = category_name if category_name else None
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

    # Associates the new ingredient with the recipe
    def add_ingredient(self, ingredient_name, recipe_id):
        ingredient = Ingredient.find_by_name(ingredient_name)
        if ingredient:
            print(f"Ingredient '{ingredient_name}' already exists.")
        else:
            self.associate_ingredient(ingredient, recipe_id)

    def associate_ingredient(self, ingredient, recipe_ids):
        if not hasattr(self, "_ingredients"):
            self._ingredients = ""

        ingredient_name = ingredient.name
        if ingredient_name not in self._ingredients:
            if self._ingredients:
                self._ingredients += ", "
            self._ingredients += ingredient_name

        # Ensure recipe_ids is a list
        if not isinstance(recipe_ids, list):
            recipe_ids = [recipe_ids]

        # Update the ingredient's recipe_ids attribute
        ingredient.recipe_id.extend(recipe_ids)

    # Associates the new category with the recipe
    def add_category(self, category_name):
        category = Category.find_by_name(category_name)
        if category:
            print(f"Category '{category_name}' already exists.")
        else:
            self.associate_category(category)

    def associate_category(self, category, recipe_ids):
        if not hasattr(self, "_categories"):
            self._categories = []

        category_name = category.name
        if category_name not in self._categories:
            self._categories.append(category_name)

        # Ensure recipe_ids is a list
        if not isinstance(recipe_ids, list):
            recipe_ids = [recipe_ids]

        # Update the category's recipe_ids attribute
        category.recipe_id.extend(recipe_ids)

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
