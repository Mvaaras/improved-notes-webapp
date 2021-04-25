from db import db

def add_tags(tags,id):
    if len(tags) == 0:
        return True
    adding = [tag.strip() for tag in tags.split(",")]
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