# src/sandbox/docker_sandbox.py

import os
import docker


class DockerSandbox:
    """
    Runs tests safely inside Docker containers.
    """

    def __init__(self):

        try:

            self.client = docker.from_env()

            self.client.ping()

            print("Docker connected!")

        except Exception as e:

            print(f"Docker not available: {e}")

            self.client = None

    def is_available(self) -> bool:
        """
        Check if Docker is available.
        """

        return self.client is not None

    def run_tests(
        self,
        codebase_path: str,
        test_command: str
    ) -> dict:
        """
        Run tests inside isolated secure Docker container.
        """

        if not self.client:

            return {
                "success": False,
                "stdout": "",
                "stderr": "Docker client unavailable",
                "exit_code": -1
            }

        abs_path = os.path.abspath(
            codebase_path
        )

        print(
            f"Starting sandbox for: {codebase_path}"
        )

        print(
            f"Running: {test_command}"
        )

        try:

            container = self.client.containers.run(

                image="python:3.11-slim",

                command=(
                    "sh -c "
                    "'pip install "
                    "pytest "
                    "pytest-cov "
                    "docker "
                    "rich "
                    "typer "
                    "watchdog "
                    "--quiet "
                    f"&& {test_command}'"
                ),

                volumes={
                    abs_path: {
                        "bind": "/app",
                        "mode": "ro"
                    }
                },

                working_dir="/app",

                detach=True,

                mem_limit="512m",

                nano_cpus=1000000000,

                network_disabled=True,

                read_only=True,

                pids_limit=100,

                security_opt=[
                    "no-new-privileges"
                ]
            )

            result = container.wait(
                timeout=60
            )

            logs = container.logs().decode(
                "utf-8"
            )

            exit_code = result.get(
                "StatusCode",
                1
            )

            container.remove(
                force=True
            )

            print("Container destroyed!")

            return {

                "success": exit_code == 0,

                "stdout": logs,

                "stderr": "",

                "exit_code": exit_code,

                "framework": test_command,

                "codebase": codebase_path
            }

        except Exception as e:

            return {

                "success": False,

                "stdout": "",

                "stderr": str(e),

                "exit_code": -1
            }