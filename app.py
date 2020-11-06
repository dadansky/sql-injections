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
        db.execute(f"SELECT secret FROM users WHERE username = '{username}' AND password = '{password}'")
        data = db.fetchone()
        if data is None:
            return "Incorrect username or password"
        else:
            return jsonify(data)


@app.route('/users')
def list_users():
    secret = request.args.get("secret")
    with Database() as db:
        db.execute(f"SELECT secret FROM users WHERE secret = '{secret}' and username = 'root'")
        data = db.fetchone()
        if data is None:
            return "Not permitted"
        else:
            db.execute(f"SELECT username, password FROM users")
            data = db.fetchall()
            return jsonify(data)


if __name__ == '__main__':
    init_dataset(10)
    app.run(debug=True)
