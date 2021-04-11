from app import app
from flask import render_template, request, redirect
import users
import notespy

#routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Registration failed")

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Login failed")

@app.route("/notes")
def notes():
    usernotes = notespy.get_notes(users.user_id())
    print(usernotes)
    return render_template("notes.html", usernotes=usernotes)


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new", methods=["get","post"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        note = request.form["notecontent"]
        if notespy.create_note(note):
            return redirect("/notes")
        else:
            return render_template("error.html",message="Creating the note failed")

@app.route("/dele", methods=["get","post"])
def dele():
    if request.method == "POST":
        deleting = request.form["id"]
        if notespy.delete(deleting):
            return redirect("/notes")
        else:
            return render_template("error.html",message="Could not delete note")
