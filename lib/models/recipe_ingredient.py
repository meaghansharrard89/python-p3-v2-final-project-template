from models.__init__ import CURSOR, CONN
from models.recipe import Recipe
from models.ingredient import Ingredient


class RecipeIngredient:
    all = {}

    def __init__(self, recipe, ingredient, id=None):
        self._id = id
        self._recipe = recipe
        self._ingredient = ingredient

    @property
    def id(self):
        return self._id

    @property
    def recipe(self):
        return self._recipe

    @property
    def ingredient(self):
        return self._ingredient

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS recipe_ingredients (
                id INTEGER PRIMARY KEY,
                recipe_id INTEGER,
                ingredient_id INTEGER,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Create new recipe
    # Update recipe
    def save(self):
        sql = """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.recipe.id, self.ingredient.id))
        CONN.commit()

    # Update recipe
    @classmethod
    def delete_by_recipe_id(cls, recipe_id):
        sql = "DELETE FROM recipe_ingredients WHERE recipe_id = ?"
        CURSOR.execute(sql, (recipe_id,))
        CONN.commit()

    # Find ingredients by recipe ID
    @classmethod
    def find_by_recipe_id(cls, recipe_id):
        sql = "SELECT ingredient_id FROM recipe_ingredients WHERE recipe_id = ?"
        rows = CURSOR.execute(sql, (recipe_id,)).fetchall()

        if rows:
            ingredient_ids = [row[0] for row in rows]
            ingredients = [
                Ingredient.find_by_id(ingredient_id).name
                for ingredient_id in ingredient_ids
            ]
            return ingredients
        else:
            return []


from models.recipe import Recipe
