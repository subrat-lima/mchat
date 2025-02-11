from mchat.model import engine
from mchat.model.user import User
from sqlmodel import Session, select


def create(user: User) -> bool:
    with Session(engine) as session:
        session.add(user)
        session.commit()
    return True


def get_by_username(username: str) -> User | None:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).one_or_none()


def get_all() -> list[User] | None:
    with Session(engine) as session:
        return session.exec(select(User)).all()
