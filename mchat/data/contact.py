from typing import Optional

import mchat.helper as db


def get_by_user(curs, user_id: int):
    statement = """
    WITH LastMessages AS (
		SELECT 
			*,
			ROW_NUMBER() OVER (PARTITION BY 
				CASE 
					WHEN sender_id < receiver_id THEN sender_id || '-' || receiver_id 
					ELSE receiver_id || '-' || sender_id 
				END 
			ORDER BY create_date ASC) AS rn
		FROM messages
		WHERE (expiry_date IS NULL OR expiry_date > CURRENT_TIMESTAMP)
	)
	SELECT 
		lm.sender_id,
		lm.receiver_id,
        lm.data,
        lm.create_date,
		u1.username AS sender_username,
		u2.username AS receiver_username
	FROM LastMessages lm
	JOIN users u1 ON lm.sender_id = u1.id
	JOIN users u2 ON lm.receiver_id = u2.id
	WHERE lm.rn = 1
    AND (lm.sender_id = :user_id OR lm.receiver_id = :user_id);
    """
    return db.all(curs, statement, {"user_id": user_id})


def get_by_user_and_date(curs, user_id: int, create_date: str):
    statement = """
    SELECT u.username, u.id
    FROM messages m
    JOIN users u ON u.id = m.sender_id
    WHERE m.receiver_id = :user_id
    AND datetime(m.create_date) >= datetime(:create_date)

    UNION

    SELECT u.username, u.id
    FROM messages m
    JOIN users u ON u.id = m.receiver_id
    WHERE m.sender_id = :user_id
    AND datetime(m.create_date) = datetime(:create_date)
    """
    return db.all(curs, statement, {"user_id": user_id, "create_date": create_date})
