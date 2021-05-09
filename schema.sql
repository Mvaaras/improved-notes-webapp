CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    note TEXT,
    visibility TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    tag TEXT
);

CREATE TABLE tagged (
    id SERIAL PRIMARY KEY,
    tag_id INTEGER REFERENCES tags,
    note_id INTEGER REFERENCES notes
);