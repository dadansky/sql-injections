import sqlite3
from flask import Flask, request, jsonify

from models import Database, init_dataset


app = Flask(__name__)

"""
Test user:
username: user1
password: password
secret: secret
"""


@app.route('/')
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    with Database() as db:
        query = "SELECT secret FROM users WHERE username = ? AND password = ?"
        params = (username, password)
        db.execute(query, params)
        data = db.fetchone()
        if data is None:
            return "Incorrect username or password"
        else:
            return jsonify({'secret': data[0]})


@app.route('/users')
def list_users():
    secret = request.args.get("secret")
    with Database() as db:
        try:
            query = f"SELECT secret FROM users WHERE secret = ? and username = 'root'"
            params = (secret,)
            print(query)
            db.execute(query, params)
            data = db.fetchone()
        except sqlite3.OperationalError:
            return jsonify({'error': "Database error"})
        if data is None:
            return jsonify({'error': "Not permitted"})
        else:
            db.execute(f"SELECT username, password FROM users")
            data = db.fetchall()
            return jsonify([{'username': datum[0], 'password': datum[1]} for datum in data])


if __name__ == '__main__':
    init_dataset(10)
    app.run(debug=True)
