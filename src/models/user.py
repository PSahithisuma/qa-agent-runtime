from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from src.db.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True
    )

    email = Column(
        String,
        unique=True
    )

    hashed_password = Column(
        String
    )

    role = Column(
        String,
        default="developer"
    )

    organization_id = Column(

        Integer,

        ForeignKey("organizations.id")
    )