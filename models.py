import os
import sqlite3
import uuid


class Database:
    def __init__(self, db_path: str = os.path.join(os.path.dirname(__file__), "db.sql")):
        self.db_path = db_path

    def __enter__(self):
        self.db_conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.db_conn.cursor()
        return self.cursor

    def __exit__(self, *args):
        self.db_conn.commit()
        self.db_conn.close()

    def __del__(self):
        self.db_conn.close()


def init_dataset(count: int) -> None:
    """
    :param count - additional users exclude root and user1:
    :return:
    """
    with Database() as db:
        db.execute("DROP TABLE IF EXISTS users")
        db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, secret TEXT)")
        db.execute(f"INSERT INTO users VALUES ('root', '{str(uuid.uuid4())}', '{str(uuid.uuid4())}')")
        db.execute("INSERT INTO users VALUES ('user1', 'password', 'secret')")
        for i in range(count):
            db.execute(f"INSERT INTO users VALUES ('user{i+2}', '{str(uuid.uuid4())}', '{str(uuid.uuid4())}')")
