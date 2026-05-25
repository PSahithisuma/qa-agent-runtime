from celery import Celery


celery = Celery(

    "qa_agent",

    broker="redis://localhost:6379/0",

    backend="redis://localhost:6379/0",

    include=[

        "src.tasks.test_tasks",

        "src.tasks.api_test_tasks"
    ]
)