from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import ForeignKey

from src.db.database import Base


class TestRun(Base):

    __tablename__ = "test_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    success = Column(Boolean)

    framework = Column(String)

    coverage = Column(String)

    logs = Column(String)

    organization_id = Column(

        Integer,

        ForeignKey("organizations.id")
    )

    project_id = Column(

        Integer,

        ForeignKey("projects.id")
    )

    user_id = Column(

        Integer,

        ForeignKey("users.id")
    )