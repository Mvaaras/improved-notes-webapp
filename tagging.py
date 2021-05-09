from db import db

def add_tags(tags,id):
    if len(tags) == 0:
        return True
    #duplicate tags are not allowed (they break stuff), so we just turn this into a set for a second to get rid of those
    #i am well aware that my method of programming involves copious amounts of ducktape and almost nothing else
    adding = list(set([tag.strip() for tag in tags.split(",")]))
    for tag in adding:
        sql_id = "SELECT id FROM tags WHERE tag =:tag"
        tag_id = db.session.execute(sql_id,{"tag":tag}).fetchone()
        if tag_id == None:
            sql = "INSERT INTO tags (tag) VALUES (:tag)"
            db.session.execute(sql,{"tag":tag})
            tag_id = db.session.execute(sql_id,{"tag":tag}).fetchone()
        sql = "INSERT INTO tagged (tag_id,note_id) VALUES (:tag,:id)"
        db.session.execute(sql,{"tag":tag_id[0],"id":id})
    db.session.commit()
    return True

def get_id(tag):
    sql = "SELECT id FROM tags WHERE tag =:tag"
    return db.session.execute(sql,{"tag":tag}).fetchone()[0]

def get_tags(id):
    sql = "SELECT t.tag FROM tags t INNER JOIN tagged tg ON t.id = tg.tag_id WHERE tg.note_id =:id"
    tags = db.session.execute(sql,{"id":id}).fetchall()
    return tags

def tag_notes(notes):
    tags = {}
    for note in notes:
        tags[note[1]] = get_tags(note[1])
    return tags

#removing tags is used when you edit them
#editing tags means that we delete all the old tags and then add new ones :)
#this only happens if you make changes to the tags though
def remove_tags(id):
    sql = "DELETE FROM tagged WHERE note_id=:note_id"
    db.session.execute(sql, {"note_id":id})
    db.session.commit()
