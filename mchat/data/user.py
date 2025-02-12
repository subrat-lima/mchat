from mchat.model.user import User, UserIn


def create(curs, user: UserIn) -> bool:
    statement = """INSERT INTO user (username, password) VALUES(?, ?)"""
    curs.execute(statement, (user.username, user.password))
    return True


def get_one(curs, id: int) -> User | None:
    statement = """SELECT * FROM user WHERE id = ?"""
    curs.execute(statement, (id,))
    user = curs.fetchone()
    if user:
        return User(**user)
    return None


def get_by_username(curs, username: str) -> User | None:
    statement = """SELECT * FROM user WHERE username = ?"""
    curs.execute(statement, (username,))
    user = curs.fetchone()
    if user:
        return User(**user)
    return None


def get_all(curs) -> list[User] | None:
    statement = """SELECT * FROM user"""
    curs.execute(statement)
    rows = curs.fetchall()
    if rows:
        users = [User(**row) for row in rows]
        return users
    return None
