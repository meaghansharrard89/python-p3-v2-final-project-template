from models.__init__ import CURSOR, CONN
from models.ingredient import Ingredient
from models.category import Category

RecipeIngredient = None  # Placeholder for now


class Recipe:
    all = {}

    def __init__(self, title, instructions, category, ingredients, id=None):
        self._id = id
        self._title = title
        self._instructions = instructions
        self._category = category
        self._ingredients = ingredients  # Change to a list

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

    def input_ingredients(self):
        ingredients_input = input(
            "Enter the ingredients for the recipe (comma-separated): "
        )
        ingredient_names = [
            ingredient.strip() for ingredient in ingredients_input.split(",")
        ]

        # Validate and add existing ingredients to the recipe
        for ingredient_name in ingredient_names:
            existing_ingredient = Ingredient.find_by_name(ingredient_name)
            if existing_ingredient:
                self._ingredients.append(existing_ingredient)
            else:
                print(
                    f"Ingredient '{ingredient_name}' not found. Creating a new ingredient."
                )
                new_ingredient = Ingredient(ingredient_name)
                new_ingredient.save()
                self._ingredients.append(new_ingredient)

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                instructions TEXT NOT NULL,
                category_id INTEGER,
                ingredients TEXT,
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

    def save(self):
        # Check if ingredients exist in Ingredients class, create new ones if needed
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

        # Save the recipe with the existing and new ingredients
        ingredients_str = ", ".join(
            ingredient.name for ingredient in existing_ingredients + new_ingredients
        )

        sql = """
            INSERT INTO recipes (title, instructions, category_id, ingredients)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(
            sql,
            (
                self.title,
                self.instructions,
                self.category.id if self.category else None,
                ingredients_str,
            ),
        )
        self._id = CURSOR.lastrowid
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM recipes WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

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
            recipe._ingredients = (
                row[4].split(", ") if row[4] else []
            )  # Split ingredients
        else:
            recipe = cls(
                row[1],
                row[2],
                Category.find_by_id(row[3]) if row[3] else None,
                row[4].split(", ") if row[4] else [],  # Split ingredients
            )
            recipe._id = row[0]
            cls.all[recipe.id] = recipe

        return recipe

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
            self.associate_ingredient(ingredient_name, recipe_id)

    def associate_ingredient(self, ingredient_name, recipe_ids):
        if not hasattr(self, "_ingredients"):
            self._ingredients = ""

        if ingredient_name not in self._ingredients:
            if self._ingredients:
                self._ingredients += ", "
            self._ingredients += ingredient_name

        # Ensure recipe_ids is a list
        if not isinstance(recipe_ids, list):
            recipe_ids = [recipe_ids]

        for recipe_id in recipe_ids:
            # Save the association in RecipeIngredient table
            recipe = Recipe.find_by_id(recipe_id)
            ingredient = Ingredient.find_by_name(ingredient_name)

            if recipe and ingredient:
                recipe_ingredient = RecipeIngredient(recipe, ingredient)
                recipe_ingredient.save()
            else:
                print("Recipe or Ingredient not found.")

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

    def update(self):
        sql = """
            UPDATE recipes
            SET title = ?, instructions = ?, category_id = ?, ingredients = ?
            WHERE id = ?
        """
        CURSOR.execute(
            sql,
            (
                self.title,
                self.instructions,
                self.category.id if self.category else None,
                ", ".join(self.ingredients) if self.ingredients else None,
                self.id,
            ),
        )
        CONN.commit()
