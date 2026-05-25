from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from src.db.database import Base


class Organization(Base):

    __tablename__ = "organizations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True
    )