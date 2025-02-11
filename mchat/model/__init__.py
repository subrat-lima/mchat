from sqlmodel import SQLModel, create_engine

from . import token, user

engine = create_engine("sqlite:///mchat.db")


SQLModel.metadata.create_all(engine)
