DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    create_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 0
);


DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    create_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(owner_id) REFERENCES users(id)
);


DROP TABLE IF EXISTS user_groups;
CREATE TABLE user_groups(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    role INTEGER NOT NULL DEFAULT 0,
    create_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(group_id) REFERENCES groups(id),
    UNIQUE(user_id, group_id)
);


DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    message TEXT NOT NULL,
    category INTEGER NOT NULL DEFAULT 0,
    sender_id INTEGER NOT NULL,
    parent_message_id INTEGER,
    create_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TEXT,
    FOREIGN KEY(sender_id) REFERENCES users(id),
    FOREIGN KEY(parent_message_id) REFERENCES messages(id)
);


DROP TABLE IF EXISTS message_recipients;
CREATE TABLE message_recipients (
    id INTEGER PRIMARY KEY,
    recipient_id INTEGER,
    recipient_group_id INTEGER,
    message_id INTEGER NOT NULL,
    status INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(recipient_id) REFERENCES users(id),
    FOREIGN KEY(recipient_group_id) REFERENCES groups(id),
    FOREIGN KEY(message_id) REFERENCES messages(id),
    UNIQUE(recipient_id, recipient_group_id, message_id)
);
