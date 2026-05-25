import asyncio

from src.tasks.celery_app import celery

from src.runner.test_runner import (
    TestRunner
)

from src.services.test_service import (
    TestService
)

from src.api.routes.ws_routes import (
    manager
)

from src.services.vector_service import (
    VectorService
)


@celery.task
def execute_tests(
    codebase_path="."
):
    """
    Execute tests asynchronously.
    """

    try:

        asyncio.run(

            manager.broadcast({

                "event": "execution_started",

                "status": "running",

                "codebase": codebase_path
            })
        )

        runner = TestRunner()

        result = runner.run(

            codebase_path=codebase_path
        )

        run_id = TestService.save_test_run(
            result
        )

        result["run_id"] = run_id

        # SAFE VECTOR STORAGE

        try:

            vector_service = VectorService()

            for idx, failure in enumerate(

                result.get("failures", [])
            ):

                vector_service.store_failure(

                    failure_id=(run_id * 1000) + idx,

                    text=failure.get(
                        "assertion_message",
                        ""
                    ),

                    metadata={

                        "test_name": failure.get(
                            "test_name"
                        ),

                        "file_path": failure.get(
                            "file_path"
                        ),

                        "line_number": failure.get(
                            "line_number"
                        ),

                        "error_type": failure.get(
                            "error_type"
                        ),

                        "run_id": run_id
                    }
                )

        except Exception as vector_error:

            print(

                f"Vector storage failed: {vector_error}"
            )

        asyncio.run(

            manager.broadcast({

                "event": "execution_completed",

                "status": "finished",

                "run_id": run_id,

                "success": result.get(
                    "success",
                    False
                )
            })
        )

        return result

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }