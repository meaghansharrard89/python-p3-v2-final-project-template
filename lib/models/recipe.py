from models.__init__ import CURSOR, CONN


class Recipe:
    all = {}

    def __init__(self, title, instructions):
        self.title = title
        self.instructions = instructions

    @classmethod
    def create_table(cls):
        # Create recipes table
        sql = """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                instructions TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        # SQL command to drop recipes table that persists Recipe instances
        sql = """
            DROP TABLE IF EXISTS recipes;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        # Insert this recipe into the database
        sql = """
            INSERT INTO recipes (title, instructions) 
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.title, self.instructions))
        CONN.commit()

    def delete(self):
        # Delete this recipe from the database
        sql = """
            DELETE FROM recipes 
            WHERE title = ?
        """
        CURSOR.execute(sql, (self.title,))
        CONN.commit()

    @classmethod
    def instance_from_db(cls, row):
        # Check the dictionary for an existing instance using the row's primary key
        recipe = cls.all.get(row[0])
        if recipe:
            # Ensure attributes match row values in case the local instance was modified
            recipe.title = row[1]
            recipe.instructions = row[2]
        else:
            # Not in dictionary, create a new instance and add it to the dictionary
            recipe = cls(row[1], row[2])
            recipe.id = row[0]
            cls.all[recipe.id] = recipe
        return recipe

    @classmethod
    def get_all(cls):
        # Return a list of all recipe instances
        sql = """
            SELECT *
            FROM recipes
        """

        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        # Find a recipe by its ID
        sql = """
            SELECT *
            FROM recipes
            WHERE id = ?
        """
        # Return Recipe object from the table row with matching primary key
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_title(cls, title):
        # Find a recipe by its title
        sql = """
            SELECT *
            FROM recipes
            WHERE title = ?
        """
        # Return Recipe object from the table row with matching title
        row = CURSOR.execute(sql, (title,)).fetchone()
        return cls.instance_from_db(row) if row else None
