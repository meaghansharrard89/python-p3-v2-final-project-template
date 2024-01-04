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

    # Create new category
    def save(self):
        sql = """
            INSERT INTO categories (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        self._id = CURSOR.lastrowid
        CONN.commit()

    # Delete category
    def delete(self):
        sql = "DELETE FROM categories WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    # Update category
    def update(self):
        sql = """
            UPDATE categories
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    # Display all categories
    @classmethod
    def get_all(cls):
        sql = "SELECT id, name FROM categories"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    # Find category by ID
    # Update category
    # Create new recipe
    # Update recipe
    @classmethod
    def find_by_id(cls, category_id):
        sql = "SELECT * FROM categories WHERE id = ?"
        row = CURSOR.execute(sql, (category_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # Find category by ID
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

    # Delete category
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM categories
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
