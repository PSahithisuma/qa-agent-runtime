from src.db.database import SessionLocal

from src.models.test_run import TestRun
from src.models.test_failure import TestFailure


class TestService:

    @staticmethod
    def save_test_run(result):

        db = SessionLocal()

        try:

            run = TestRun(

                success=result.get("success"),

                framework=result.get(
                    "framework_detected"
                ),

                coverage=result.get(
                    "coverage"
                ),

                logs=result.get(
                    "stdout"
                )
            )

            db.add(run)

            db.commit()

            db.refresh(run)

            run_id = run.id

            failures = result.get(
                "failures",
                []
            )

            for failure in failures:

                db_failure = TestFailure(

                    run_id=run_id,

                    test_name=failure.get(
                        "test_name"
                    ),

                    error_type=failure.get(
                        "error_type"
                    ),

                    assertion_message=failure.get(
                        "assertion_message"
                    ),

                    file_path=failure.get(
                        "file_path"
                    ),

                    line_number=failure.get(
                        "line_number"
                    )
                )

                db.add(db_failure)

            db.commit()

            return run_id

        finally:

            db.close()