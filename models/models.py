from typing import Optional
import enum

from sqlalchemy import (Column, Integer)
from sqlalchemy_utils import ChoiceType
from sqlmodel import Field, Session, SQLModel, create_engine, select


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


class Rating(enum.IntEnum):
    Unrated = 0
    Low = 1
    Medium = 2
    High = 3


class Projectinfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    priority: Rating = Field(sa_column=Column(ChoiceType(Rating, impl=Integer()), nullable=True), default=Rating.Unrated)
    owner: Optional[str]
    load: Rating = Field(sa_column=Column(ChoiceType(Rating, impl=Integer()), nullable=False), default=Rating.Low)
    owner: Optional[str]
    deadline: Optional[int] = None

    def save_to_database(self):
        with Session(engine) as session:
            session.add(self)
            session.commit()

    @property
    def loadAsString(self):
        return self.load.name

    @property
    def priorityAsString(self):
        if self.priority is Rating.Unrated:
            return ""
        return self.load.name

    def get_projectinfo():
        with Session(engine) as session:
            statement = select(Projectinfo)
            results = session.exec(statement).all()
            return results


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    full_name: str    
    hashed_password: str

    def save_to_database(self):
        with Session(engine) as session:
            session.add(self)
            session.commit()

    def get_users():
        with Session(engine) as session:
            statement = select(User)
            results = session.exec(statement).all()
            return results


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
