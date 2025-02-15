INSERT INTO content_type(id, name) VALUES
(1, "TEXT"),
(2, "AUDIO"),
(3, "VIDEO"),
(4, "ATTACHMENT") ON CONFLICT(name) DO NOTHING;


INSERT INTO role(id, name) VALUES
    (1, "ADMIN"),
    (2, "MEMBER") ON CONFLICT(name) DO NOTHING;


INSERT INTO chat_type(id, name) VALUES
    (1, "DIRECT"),
    (2, "GROUP") ON CONFLICT(name) DO NOTHING;
