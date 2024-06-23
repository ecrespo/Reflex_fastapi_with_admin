import enum

from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Enum, String
from sqlalchemy.types import TypeDecorator, Text

from Reflex_fastapi_with_admin.databases.database import Base


class Status(str, enum.Enum):
    Draft = "d"
    Published = "p"
    Withdrawn = "w"


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(Enum(Status))
