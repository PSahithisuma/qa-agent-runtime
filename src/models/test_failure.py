from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from src.db.database import Base


class TestFailure(Base):

    __tablename__ = "test_failures"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    run_id = Column(
        Integer,
        ForeignKey("test_runs.id")
    )

    test_name = Column(String)

    error_type = Column(String)

    assertion_message = Column(String)

    file_path = Column(String)

    line_number = Column(Integer)