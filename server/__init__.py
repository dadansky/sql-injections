from flask import Flask, request, jsonify, render_template, redirect, session
import uuid
import os
from server.models import User, News

app = Flask(__name__)
app.config["SECRET_KEY"] = str(uuid.uuid4())


@app.route('/', methods=["GET"])
@app.route("/login", methods=["POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    username = request.form.get("username")
    password = request.form.get("password")
    with User() as users:
        user = users.find_user(username, password)
    if user and users.is_admin(username):
        session["current_user"] = user[0]
        session.modified = True
        return redirect("/admin")
    elif user:
        session["current_user"] = user[0]
        session.modified = True
        return redirect("/news")
    else:
        return redirect("/")


@app.route('/news')
def get_news():
    if session.get("current_user"):
        with News() as news:
            return render_template("news.html", news=news.get_all_news())
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session["current_user"] = None
    session.modified = True
    return redirect("/")


@app.route('/news/<title>')
def new_detail(title):
    return ""


@app.route('/admin')
def admin_panel():
    with User() as users:
        if session.get("current_user") and users.is_admin(session.get("current_user")):
            return render_template("admin_panel.html", users=users.get_users())
        else:
            return redirect("/")
