import sqlite3

CONN = sqlite3.connect("recipe_organizer.db")
CURSOR = CONN.cursor()
