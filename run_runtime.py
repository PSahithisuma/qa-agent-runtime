
import subprocess


subprocess.Popen([
    "uvicorn",
    "src.api.main:app",
    "--reload"
])

subprocess.Popen([
    "celery",
    "-A",
    "src.tasks.test_tasks",
    "worker",
    "--pool=solo",
    "--loglevel=info"
])

print("QA Runtime Started")