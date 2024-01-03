from models.__init__ import CURSOR, CONN
from models.recipe import Recipe
from models.ingredient import Ingredient
from rich.console import Console
from rich.table import Table


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

    @classmethod
    def display_table_schema(cls):
        console = Console()
        table = Table(title="[bold blue]Recipe Ingredients Table Schema[/bold blue]")

        table.add_column("[green]Column[/green]")
        table.add_column("[green]Data Type[/green]")
        table.add_column("[green]Constraints[/green]")

        schema = [
            ("id", "INTEGER", "PRIMARY KEY"),
            ("recipe_id", "INTEGER", "FOREIGN KEY (recipe_id) REFERENCES recipes(id)"),
            (
                "ingredient_id",
                "INTEGER",
                "FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)",
            ),
        ]

        for column, data_type, constraints in schema:
            table.add_row(column, data_type, constraints)

        console.print(table)

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
            print(f"No ingredients found for recipe with ID {recipe_id}")
            return []


from models.recipe import Recipe
