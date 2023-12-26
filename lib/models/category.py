from models.__init__ import CURSOR, CONN


class Category:
    all = {}

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls):
        # Create categories table
        sql = """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        # SQL command to drop category table that persists Category instances
        sql = """
            DROP TABLE IF EXISTS categories;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        # Insert this category into the database
        sql = """
            INSERT INTO categories (name) 
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        CONN.commit()

    def delete(self):
        # Delete this category from the database
        sql = """
            DELETE FROM categories 
            WHERE name = ?
        """
        CURSOR.execute(sql, (self.name,))
        CONN.commit()

    @classmethod
    def instance_from_db(cls, row):
        # Check the dictionary for an existing instance using the row's primary key
        category = cls.all.get(row[0])
        if category:
            # Ensure attributes match row values in case the local instance was modified
            category.name = row[1]
        else:
            # Not in dictionary, create a new instance and add it to the dictionary
            category = cls(row[1])
            category.id = row[0]
            cls.all[category.id] = category
        return category

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM categories
        """
        rows = CURSOR.execute(sql).fetchall()

        # Clear the existing categories dictionary before populating it
        cls.all = {}

        categories = [cls.instance_from_db(row) for row in rows]

        # Populate the categories dictionary with the new data
        for category in categories:
            cls.all[category.id] = category

        return categories

    @classmethod
    def find_by_id(cls, id):
        # Find a category by its ID
        sql = """
            SELECT *
            FROM categories
            WHERE id = ?
        """
        # Return Category object from the table row with matching primary key
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        # Find a category by its name
        sql = """
            SELECT *
            FROM categories
            WHERE name = ?
        """
        # Return Category object from the table row with matching name
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None