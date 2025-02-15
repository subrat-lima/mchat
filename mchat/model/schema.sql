CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_active INTEGER DEFAULT 0
);


CREATE TABLE IF NOT EXISTS contact (
    user_id  INTEGER NOT NULL,
    friend_id  INTEGER NOT NULL,
    alias TEXT NOT NULL,
    UNIQUE(user_id, friend_id),
    UNIQUE(user_id, alias),
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(friend_id) REFERENCES user(id)
);


CREATE TABLE IF NOT EXISTS role(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);




CREATE TABLE IF NOT EXISTS content_type(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS chat_type(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);



CREATE TABLE IF NOT EXISTS chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_type_id INTEGER NOT NULL,
    FOREIGN KEY(chat_type_id) REFERENCES chat_type(id)
);


CREATE TABLE IF NOT EXISTS member (
    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    joined_at TEXT NOT NULL DEFAULT current_timestamp,
    left_at TEXT,
    FOREIGN KEY(chat_id) REFERENCES chat(id),
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(role_id) REFERENCES role(id)
);


CREATE TABLE IF NOT EXISTS message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content_type_id INTEGER NOT NULL DEFAULT 1,
    content TEXT,
    UNIQUE(chat_id, user_id, content_type_id, content),
    FOREIGN KEY(chat_id) REFERENCES chat(id),
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(content_type_id) REFERENCES user(content_type)
); 
