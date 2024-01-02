from models.__init__ import CURSOR, CONN


class Category:
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
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS categories"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO categories (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        self._id = (
            CURSOR.lastrowid
        )  # Retrieve the last inserted row ID and store it as the object's ID
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM categories WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    def update(self):
        sql = """
            UPDATE categories
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    # def update_recipe_ids(self):
    #     sql = """
    #         UPDATE categories
    #         SET recipe_id = ?
    #         WHERE id = ?
    #     """
    #     # For updating multipe recipe IDs
    #     CURSOR.execute(sql, (",".join(map(str, self.recipe_id)), self.id))
    #     CONN.commit()

    @classmethod
    def get_all(cls):
        sql = "SELECT id, name FROM categories"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def instance_from_db(cls, row):
        category = cls.all.get(row[0])
        if category:
            category.name = row[1]
        else:
            category = cls(row[1])
            category._id = row[0]
            cls.all[category.id] = category
        return category

    @classmethod
    def find_by_id(cls, category_id):
        sql = "SELECT * FROM categories WHERE id = ?"
        row = CURSOR.execute(sql, (category_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # @classmethod
    # def find_recipe_id_by_name(cls, name):
    #     # Find a category's recipe ID by its name
    #     sql = """
    #         SELECT recipe_id
    #         FROM categories
    #         WHERE name = ?
    #     """
    #     # Return the recipe ID(s)
    #     row = CURSOR.execute(sql, (name,)).fetchone()
    #     return row[0] if row else None

    @classmethod
    def find_by_name(cls, name):
        # Find a category by its name
        sql = """
            SELECT *
            FROM categories
            WHERE name = ?
        """
        # Return the first table row of a Category object matching a name
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
