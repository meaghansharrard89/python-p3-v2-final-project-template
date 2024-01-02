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

    def save(self):
        sql = """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.recipe.id, self.ingredient.id))
        CONN.commit()

    @classmethod
    def find_by_recipe_and_ingredient(cls, recipe, ingredient):
        sql = """
            SELECT * FROM RecipeIngredient
            WHERE recipe_id = ? AND ingredient_id = ?
        """
        params = (recipe.id, ingredient.id)
        row = CURSOR.execute(sql, params).fetchone()
        return cls.instance_from_db(row) if row and recipe and ingredient else None

    @classmethod
    def instance_from_db(cls, row):
        if row is None:
            return None

        recipe_id, ingredient_id = row
        recipe = Recipe.find_by_id(recipe_id)
        ingredient = Ingredient.find_by_id(ingredient_id)

        if recipe and ingredient:
            return cls(recipe, ingredient, id=row[0])
        else:
            return None

    @classmethod
    def delete_by_recipe_id(cls, recipe_id):
        sql = "DELETE FROM recipe_ingredients WHERE recipe_id = ?"
        CURSOR.execute(sql, (recipe_id,))
        CONN.commit()


from models.recipe import Recipe
