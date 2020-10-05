import os
import sqlite3


class Database:
    table_name = ""

    def __init__(self, db_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)))):
        self.__db_conn = sqlite3.connect(db_path)
        self.cursor = self.__db_conn.cursor()

    def filter_by(self, field, value):
        self.cursor.execute(f"SELECT * from {self.table_name} WHERE {field} = '{value}'")
        return self.cursor.fetchall()

    def find_one(self, field, value):
        self.cursor.execute(f"SELECT * from {self.table_name} WHERE {field} = '{value}'")
        return self.cursor.fetchone()

    def add(self, *values):
        add_values = f"INSERT INTO {self.table_name} VALUES=(" + ",".join(f"'{v}'" for v in values) + ")"
        self.cursor.execute(add_values)
        self.__db_conn.commit()

    def __del__(self):
        self.__db_conn.close()


class News(Database):
    table_name = "news"

    def _create_table(self):
        self.cursor.execute("""CREATE TABLE news (id text, title text, content text)""")

    def filter_by_title(self, title):
        return self.filter_by("title", title)


class User(Database):
    table_name = "users"

    def _create_table(self):
        self.cursor.execute(
            f"""CREATE TABLE {self.table_name} (id text, username text, mail text, password text, superuser bit)""")

    def find_user(self, username, password):
        self.cursor.execute(
            f"SELECT * from {self.table_name} WHERE username = '{username}' adn password = '{password}'")
        return self.cursor.fetchone()







