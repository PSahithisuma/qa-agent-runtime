from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
import subprocess
import sys


IGNORE_DIRS = [
    "__pycache__",
    ".pytest_cache",
    "venv",
    ".git"
]


class ChangeHandler(FileSystemEventHandler):

    def on_modified(self, event):

        # Ignore internal folders
        for ignored in IGNORE_DIRS:

            if ignored in event.src_path:
                return

        # Watch only Python files
        if event.src_path.endswith(".py"):

            print(f"\nFile changed: {event.src_path}")

            print("Running QA pipeline...\n")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "src.cli.main",
                    "run"
                ]
            )


if __name__ == "__main__":

    path = "."

    event_handler = ChangeHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        path,
        recursive=True
    )

    observer.start()

    print("Watching project for file changes...")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()