from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from src.db.database import Base


class Project(Base):

    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    repository_url = Column(String)

    organization_id = Column(

        Integer,

        ForeignKey("organizations.id")
    )