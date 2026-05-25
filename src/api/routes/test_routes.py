from fastapi import APIRouter
from fastapi import Depends

from celery.result import AsyncResult

from src.tasks.test_tasks import (
    execute_tests
)

from src.tasks.celery_app import (
    celery
)

from src.auth.dependencies import (
    get_current_user
)

from src.auth.rbac import (
    require_role
)

router = APIRouter()


@router.post("/run-tests")
async def run_tests(

    user=Depends(get_current_user)
):
    """
    Run tests asynchronously.
    """

    require_role(

        user["role"],

        ["admin", "developer"]
    )

    task = execute_tests.delay(".")

    return {

        "task_id": task.id,

        "status": "queued"
    }


@router.get("/tasks/{task_id}")
async def get_task_status(

    task_id: str,

    user=Depends(get_current_user)
):
    """
    Get async task status.
    """

    require_role(

        user["role"],

        ["admin", "developer", "viewer"]
    )

    task_result = AsyncResult(

        task_id,

        app=celery
    )

    response = {

        "task_id": task_id,

        "status": task_result.status
    }

    if task_result.ready():

        response["result"] = (

            task_result.result
        )

    return response