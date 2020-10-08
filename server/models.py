import os
import sqlite3
import uuid

from server.utils import exception_pass


class Database:
    table_name = ""

    def __init__(self, db_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sql")):
        self.db_path = db_path

    def __enter__(self):
        self.db_conn = sqlite3.connect(self.db_path)
        self.cursor = self.db_conn.cursor()
        return self

    def __exit__(self):
        self.db_conn.commit()
        self.db_conn.close()

    @exception_pass
    def filter_by(self, field, value):
        self.cursor.execute(f"SELECT * from {self.table_name} WHERE {field} = '{value}'")
        return self.cursor.fetchall()

    @exception_pass
    def find_one(self, field, value):
        self.cursor.execute(f"SELECT * from {self.table_name} WHERE {field} = '{value}'")
        return self.cursor.fetchone()

    @exception_pass
    def add(self, *values):
        add_values = f"INSERT INTO {self.table_name} VALUES ("
        for v in values:
            add_values += f"'{v}', "
        add_values = add_values[:len(add_values)-2] + ")"
        self.cursor.execute(add_values)

    def __del__(self):
        self.db_conn.close()


class News(Database):
    table_name = "news"

    def _create_table(self):
        try:
            self.cursor.execute("""CREATE TABLE news (id text, title text, content text)""")
            self.db_conn.commit()
        except Exception as exc:
            print("Error ",  str(exc))
            pass

    def filter_by_title(self, title):
        return self.filter_by("title", title)

    def get_all_news(self):
        try:
            self.cursor.execute(f"SELECT title from {self.table_name}")
            return self.cursor.fetchall()
        except Exception as exc:
            print(exc)
            return []


class User(Database):
    table_name = "users"

    @exception_pass
    def _create_table(self):
        self.cursor.execute(
            f"""CREATE TABLE {self.table_name} (id text, username text, mail text, password text, superuser bit)""")
        self.db_conn.commit()

    @exception_pass
    def find_user(self, username, password):
        self.cursor.execute(
            f"SELECT username, mail from {self.table_name} WHERE username = '{username}' and password = '{password}'")
        return self.cursor.fetchone()

    def is_admin(self, username):
        user = self.find_one("username", username)
        if user and user[-1] == 1:
            return True
        return False

    @exception_pass
    def get_users(self, username):
        if not self.is_admin(username):
            return []
        self.cursor.execute(f"SELECT id username mail from {self.table_name}")
        return self.cursor.fetchall()


def base_example(db_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sql")):
    if os.path.exists(db_path):
        os.remove(db_path)
    users = [
        {"username": "admin", "password": "uspertop", "mail": "admin_sql@gmail.ja", "superuser": 1},
        {"username": "Ivan", "password": "1234", "mail": "ivan1995@mail.com", "superuser": 0},
        {"username": "Betty", "password": "qwerty", "mail": "betty2000@mail.com", "superuser": 0}
    ]
    news = [
        {"title": "SQLi", "content": "You can try extract this data."},
        {"title": "Authentication", "content": "Required protected password with hashing."},
        {"title": "Secret base", "content": "Extracting secret availbale for admin user."},
        {"title": "Passwords", "content": "Save passwords as plain text is a not good idea."}
    ]
    with User(db_path) as users_m, News(db_path) as news_m:
        users_m.create_table()
        news_m.create_table()

        for user in users:
            users_m.add(str(uuid.uuid4()), user["username"], user["mail"], user["password"], user["superuser"])

        for new in news:
            news_m.add(str(uuid.uuid4()), new["title"], new["content"])
