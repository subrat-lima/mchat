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
