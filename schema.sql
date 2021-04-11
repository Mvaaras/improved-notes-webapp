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