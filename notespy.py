from db import db
import users
import tagging
from flask import session

#note visibility; 'd' for deleted (not visible to anyone), 'h' for hidden (visible to the person who created the note) and 'p' for public (visible to anyone on the creator's profilem not yet implemented)

def get_notes(id):
    sql = "SELECT note, id FROM notes WHERE user_id=:id AND notes.visibility <> 'd'"
    result = db.session.execute(sql, {"id":id})
    notes = result.fetchall()
    return notes

def get_one(id):
    sql = "SELECT note, id FROM notes WHERE id =:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result

#Creating empty notes is allowed because it doesn't really matter? It's not like they can't be edited later, if someone wants to have empty notes, I say let them :--)
def create_note(note):
    
    try:
        id = users.user_id()
        sql = "INSERT INTO notes (note,user_id,visibility) VALUES (:note,:user_id,:visibility)"
        db.session.execute(sql, {"note":note,"user_id":id,"visibility":"h"})
        
        sql = "SELECT id FROM notes WHERE note =:note"
        returning = db.session.execute(sql,{"note":note}).fetchone()[0]
        db.session.commit()
    except: 
        return False
    return returning

def edit_note(note,id):
    try:
        sql = "UPDATE notes SET note = :note WHERE id=:id"
        db.session.execute(sql, {"note":note,"id":id})
        db.session.commit()
    except:
        return False
    return True

#"delete" doesn't actually delete the note, just sets the visibility to 'd' (deleted) and removes the contents. basically the same thing as far as the user is concerned, as deleted notes never show up.
def delete(id,user):
    sql = "SELECT user_id FROM notes WHERE id=:id"
    verify = db.session.execute(sql, {"id":id}).fetchall()
    if str(user) != str(verify[0][0]):
        return False
    sql = "UPDATE notes SET visibility = 'd', note = ' ' WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True

def get_tagged(tag,id):
    tag_id = tagging.get_id(tag)
    sql = "SELECT note, notes.id FROM notes INNER JOIN tagged ON notes.id = tagged.note_id WHERE user_id=:id AND notes.visibility <> 'd' AND tagged.tag_id = :tag"
    notes = db.session.execute(sql, {"id":id,"tag":tag_id}).fetchall()
    return notes