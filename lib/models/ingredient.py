from models.__init__ import CURSOR, CONN


class Ingredient:
    all = {}

    def __init__(self, name, id=None):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
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
        sql = """
            INSERT INTO ingredients (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        self._id = (
            CURSOR.lastrowid
        )  # Retrieve the last inserted row ID and store it as the object's ID
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM ingredients WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    def update(self):
        sql = """
            UPDATE ingredients
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    # def update_recipe_ids(self):
    #     sql = """
    #         UPDATE ingredients
    #         SET recipe_id = ?
    #         WHERE id = ?
    #     """
    #     # For updating multipe recipe IDs
    #     CURSOR.execute(sql, (",".join(map(str, self.recipe_id)), self.id))
    #     CONN.commit()

    @classmethod
    def get_all(cls):
        sql = "SELECT id, name FROM ingredients"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def instance_from_db(cls, row):
        if row is None:
            return None

        ingredient = cls.all.get(row[0])
        if ingredient:
            ingredient.name = row[1] if len(row) > 1 else None
        else:
            ingredient = cls(row[1] if len(row) > 1 else None)
            ingredient._id = row[0]
            cls.all[ingredient._id] = ingredient
        return ingredient

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
