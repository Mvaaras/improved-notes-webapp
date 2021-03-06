from app import app
from flask import render_template, request, redirect
import users
import notespy
import tagging

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
        registration = users.register(username,password)
        if registration == True:
            return redirect("/")
        else:
            return render_template("error.html",message=registration)

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
    tags = tagging.tag_notes(usernotes)
    return render_template("notes.html", usernotes=usernotes, tags = tags)


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
        tags = request.form["tags"]
        id = notespy.create_note(note)
        if id:
            if tagging.add_tags(tags,id):
                return redirect("/notes")
        else:
            return render_template("error.html",message="Creating the note failed")

@app.route("/dele", methods=["get","post"])
def dele():
    if request.method == "POST":
        deleting = request.form["id"]
        if notespy.delete(deleting,request.form["user"]):
            return redirect("/notes")
        else:
            return render_template("error.html",message="Could not delete note")


#e as in editing, f as in finished
@app.route("/edit", methods=["get","post"])
def edit():
    if request.method == "POST" and request.form["status"] == 'e':
        editing = request.form["id"]
        note=notespy.get_one(editing)
        tags=tagging.get_tags(editing)
        tagsstr = ""
        for tag in tags:
            tagsstr += tag[0] + ", "
        return render_template("edit.html",note=note,tags=tagsstr[:-2])
    elif request.form["status"] == 'f':
        note = request.form["notecontent"]
        id = request.form["id"]
        if notespy.edit_note(note,id):
            if request.form["tags"] != request.form["old_tags"]:
                tagging.remove_tags(id)
                tagging.add_tags(request.form["tags"],id)
            return redirect("/notes")
        else:
            return render_template("error.html",message="Editing the note failed")
        
    else: return render_template("error.html",message="Yeah something clearly went wrong, I have no idea what it was, I have never seen this error message in action and I really don't plan to either. Applause to you for making it happen, I guess.")

@app.route("/tag/<string:tag>")
def tag(tag):
    tagnotes = notespy.get_tagged(tag,users.user_id())
    tags = tagging.tag_notes(tagnotes)
    return render_template("tag.html", tagnotes=tagnotes, tags = tags,tag=tag)


