from models.__init__ import CURSOR, CONN

class Ingredient:
    all = {}

    def __init__(self, name, recipe_id=None, id=None):
        self._id = id
        self._name = name
        self._recipe_id = recipe_id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value):
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def recipe_id(self):
        return self._recipe_id

    @recipe_id.setter
    def recipe_id(self, value):
        self._recipe_id = value

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                recipe_id INTEGER,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id)
                )
            """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS ingredients"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        # Insert this ingredient into the database
        sql = """
            INSERT INTO ingredients (name, recipe_id)
            VALUES (?, ?)
        """
        # Use the recipe_id attribute directly in the execute call
        CURSOR.execute(sql, (self.name, self.recipe_id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM ingredients WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def instance_from_db(cls, row):
        ingredient = cls.all.get(row[0])
        if ingredient:
            ingredient.name = row[1]
        else:
            ingredient = cls(row[1])
            ingredient._id = row[0]
            cls.all[ingredient.id] = ingredient
        return ingredient

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM ingredients"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, ingredient_id):
        sql = "SELECT * FROM ingredients WHERE id = ?"
        row = CURSOR.execute(sql, (ingredient_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        # Find an ingredient by its name
        sql = """
            SELECT *
            FROM ingredients
            WHERE name = ?
        """
        # Return the first table row of an Ingredient object matching a name
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
