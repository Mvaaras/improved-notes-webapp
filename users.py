from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app

def login(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["username"] = username
            return True
        else:
            return False

def register(username,password):
    if len(username) == 0:
        return "Username can't be empty" 
    if len(password) < 4:
        return "Password must be at least 4 characters long"
        
    hash_value = generate_password_hash(password)

    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return "Registration Failed"

    return login(username,password)

def user_id():
    return session.get("user_id",0)

def logout():
    del session["user_id"]