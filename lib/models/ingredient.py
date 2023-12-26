from models.__init__ import CURSOR, CONN


class Ingredient:
    all = {}

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls):
        # Create ingredients table
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
        # SQL command to drop ingredients table that persists Ingredient instances
        sql = """
            DROP TABLE IF EXISTS ingredients;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        # Insert this ingredient into the database
        sql = """
            INSERT INTO ingredients (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        CONN.commit()

    def delete(self):
        # Delete this ingredient from the database
        sql = """
            DELETE FROM ingredients 
            WHERE name = ?
        """
        CURSOR.execute(sql, (self.name,))
        CONN.commit()

    @classmethod
    def instance_from_db(cls, row):
        # Check the dictionary for an existing instance using the row's primary key
        ingredient = cls.all.get(row[0])
        if ingredient:
            # Ensure attributes match row values in case the local instance was modified
            ingredient.name = row[1]
        else:
            # Not in dictionary, create a new instance and add it to the dictionary
            ingredient = cls(row[1])
            ingredient.id = row[0]
            cls.all[ingredient.id] = ingredient
        return ingredient

    @classmethod
    def get_all(cls):
        # Return a list of all ingredient instances
        sql = """
            SELECT *
            FROM ingredients
        """

        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        # Find an ingredient by its ID
        sql = """
            SELECT *
            FROM ingredients
            WHERE id = ?
        """
        # Return Ingredient object from the table row with matching primary key
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        # Find an ingredient by its name
        sql = """
            SELECT *
            FROM ingredients
            WHERE name = ?
        """
        # Return Ingredient object from the table row with matching name
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    from models.__init__ import CURSOR, CONN