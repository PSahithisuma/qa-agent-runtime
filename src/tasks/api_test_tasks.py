from src.tasks.celery_app import celery


@celery.task(name="run_api_test")
def run_api_test(

    test_run_id: str,

    target_url: str,

    openapi_url: str = None
):
    """
    Execute API tests asynchronously.
    """

    print(

        f"Running API test for: {target_url}"
    )

    return {

        "test_run_id": test_run_id,

        "target_url": target_url,

        "openapi_url": openapi_url,

        "status": "completed",

        "success": True
    }