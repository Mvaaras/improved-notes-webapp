from db import db
import users

def get_notes(id):
    sql = "SELECT note, id FROM notes WHERE user_id=:id AND notes.visibility <> 'd'"
    print(id)
    result = db.session.execute(sql, {"id":id})
    notes = result.fetchall()
    return notes

def create_note(note):
    
    try:
        id = users.user_id()
        sql = "INSERT INTO notes (note,user_id,visibility) VALUES (:note,:user_id,:visibility)"
        db.session.execute(sql, {"note":note,"user_id":id,"visibility":"h"})
        db.session.commit()
    except: 
        return False
    return True

def delete(id):
    sql = "UPDATE notes SET visibility = 'd', note = ' ' WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True
