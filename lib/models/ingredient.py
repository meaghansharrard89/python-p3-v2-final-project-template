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

    # Create new ingredient
    # Create new recipe
    # Update recipe
    def save(self):
        sql = """
            INSERT INTO ingredients (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        self._id = CURSOR.lastrowid
        CONN.commit()

    # Delete ingredient
    def delete(self):
        sql = "DELETE FROM ingredients WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    # Update ingredient
    def update(self):
        sql = """
            UPDATE ingredients
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    # Display all ingredients
    @classmethod
    def get_all(cls):
        sql = "SELECT id, name FROM ingredients"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    # Find ingredient by ID
    # Update ingredient
    # Create new recipe
    # Update recipe
    # Find ingredients by recipe ID
    @classmethod
    def find_by_id(cls, ingredient_id):
        sql = "SELECT * FROM ingredients WHERE id = ?"
        row = CURSOR.execute(sql, (ingredient_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

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

    # Delete ingredient
    # Create new recipe
    # Update recipe
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM ingredients
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
