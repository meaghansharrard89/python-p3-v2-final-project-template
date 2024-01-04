from models.__init__ import CURSOR, CONN
from models.ingredient import Ingredient
from models.category import Category

RecipeIngredient = None


class Recipe:
    all = {}

    def __init__(self, title, instructions, category, ingredients, id=None):
        self._id = id
        self._title = title
        self._instructions = instructions
        self._category = category
        self._ingredients = ingredients

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
    def instructions(self):
        return self._instructions

    @instructions.setter
    def instructions(self, instructions):
        self._instructions = instructions

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
                title TEXT NOT NULL,
                instructions TEXT NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES category(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS recipes"
        CURSOR.execute(sql)
        CONN.commit()

    # Create new recipe
    def save(self):
        existing_ingredients = [
            Ingredient.find_by_name(ingredient) for ingredient in self.ingredients
        ]
        new_ingredients = [
            ingredient
            for ingredient in self.ingredients
            if Ingredient.find_by_name(ingredient) is None
        ]

        for new_ingredient in new_ingredients:
            ingredient = Ingredient(new_ingredient)
            ingredient.save()

        ingredients_str = ", ".join(
            ingredient.name for ingredient in existing_ingredients + new_ingredients
        )

        sql = """
            INSERT INTO recipes (title, instructions, category_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(
            sql,
            (
                self.title,
                self.instructions,
                self.category.id if self.category else None,
            ),
        )
        self._id = CURSOR.lastrowid
        CONN.commit()

    # Delete recipe
    def delete(self):
        sql = "DELETE FROM recipes WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    # Display all recipes
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM recipes"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def instance_from_db(cls, row):
        recipe = cls.all.get(row[0])
        if recipe:
            recipe.title = row[1]
            recipe.instructions = row[2]
            recipe._category = Category.find_by_id(row[3]) if row[3] else None
            recipe._ingredients = row[4].split(", ") if len(row) > 4 and row[4] else []
        else:
            recipe = cls(
                row[1],
                row[2],
                Category.find_by_id(row[3]) if row[3] else None,
                row[4].split(", ") if len(row) > 4 and row[4] else [],
            )
            recipe._id = row[0]
            cls.all[recipe.id] = recipe

        return recipe

    # Find recipe by ID
    # Update recipe
    @classmethod
    def find_by_id(cls, recipe_id):
        sql = "SELECT * FROM recipes WHERE id = ?"
        row = CURSOR.execute(sql, (recipe_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

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

        if not isinstance(recipe_ids, list):
            recipe_ids = [recipe_ids]

        category.recipe_id.extend(recipe_ids)

    # Delete recipe
    @classmethod
    def find_by_title(cls, title):
        sql = """
            SELECT *
            FROM recipes
            WHERE title = ?
        """
        row = CURSOR.execute(sql, (title,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # Update recipe
    def update(self):
        sql = """
            UPDATE recipes
            SET title = ?, instructions = ?, category_id = ?
            WHERE id = ?
        """
        CURSOR.execute(
            sql,
            (
                self.title,
                self.instructions,
                self.category.id if self.category else None,
                self.id,
            ),
        )
        CONN.commit()
