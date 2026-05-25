import os
import re
from pathlib import Path

from src.sandbox.docker_sandbox import DockerSandbox
from src.parser.failure_parser import parse_failures


class TestRunner:
    """
    Detects project test framework
    and runs tests inside Docker sandbox.
    """

    def __init__(self):

        self.sandbox = DockerSandbox()

    def detect_framework(
        self,
        codebase_path: str
    ) -> str:
        """
        Auto detect test framework.
        """

        path = Path(codebase_path)

        # Pytest
        if (path / "pytest.ini").exists():

            return (
                "pytest tests/ -v "
                "--cov=src "
                "--cov-report=term "
                "--cov-config=/dev/null "
                "--cov-append"
            )

        if (path / "pyproject.toml").exists():

            content = (
                path / "pyproject.toml"
            ).read_text()

            if "pytest" in content:

                return (
                    "pytest tests/ -v "
                    "--cov=src "
                    "--cov-report=term "
                    "--cov-config=/dev/null "
                    "--cov-append"
                )

        if (path / "setup.cfg").exists():

            content = (
                path / "setup.cfg"
            ).read_text()

            if "pytest" in content:

                return (
                    "pytest tests/ -v "
                    "--cov=src "
                    "--cov-report=term "
                    "--cov-config=/dev/null "
                    "--cov-append"
                )

        # Jest / Vitest
        if (path / "package.json").exists():

            content = (
                path / "package.json"
            ).read_text()

            if "jest" in content:

                return "npx jest --coverage"

            if "vitest" in content:

                return "npx vitest run"

        # Go
        if (path / "go.mod").exists():

            return "go test ./..."

        # Maven
        if (path / "pom.xml").exists():

            return "mvn test"

        # Gradle
        if (path / "build.gradle").exists():

            return "./gradlew test"

        # Default Python fallback
        if list(path.glob("**/*.py")):

            return (
                "pytest tests/ -v "
                "--cov=src "
                "--cov-report=term "
                "--cov-config=/dev/null "
                "--cov-append"
            )

        return "pytest tests/ -v"

    def run(
        self,
        codebase_path=".",
        framework=None
    ) -> dict:
        """
        Run tests inside Docker sandbox.
        """

        if not os.path.exists(codebase_path):

            return {

                "success": False,

                "error": (
                    f"Path not found: "
                    f"{codebase_path}"
                ),

                "stdout": "",

                "stderr": "",

                "exit_code": -1
            }

        # Auto detect framework
        if framework is None:

            framework = self.detect_framework(
                codebase_path
            )

            print(
                f"Detected framework: "
                f"{framework}"
            )

        # Run tests
        result = self.sandbox.run_tests(

            codebase_path=codebase_path,

            test_command=framework
        )

        # Add metadata
        result["framework_detected"] = framework

        result["total_tests"] = (
            self._parse_test_count(
                result.get("stdout", "")
            )
        )

        result["failed_tests"] = (
            self._parse_failed_count(
                result.get("stdout", "")
            )
        )

        result["passed_tests"] = (

            result["total_tests"]

            - result["failed_tests"]
        )

        result["coverage"] = (
            self._parse_coverage(
                result.get("stdout", "")
            )
        )

        # Structured failures
        result["failures"] = (
            parse_failures(
                result.get("stdout", "")
            )
        )

        return result

    def _parse_test_count(
        self,
        stdout: str
    ) -> int:
        """
        Parse total tests.
        """

        passed_match = re.search(
            r"(\d+) passed",
            stdout
        )

        failed_match = re.search(
            r"(\d+) failed",
            stdout
        )

        passed = (
            int(passed_match.group(1))
            if passed_match
            else 0
        )

        failed = (
            int(failed_match.group(1))
            if failed_match
            else 0
        )

        return passed + failed

    def _parse_failed_count(
        self,
        stdout: str
    ) -> int:
        """
        Parse failed test count.
        """

        failed_match = re.search(
            r"(\d+) failed",
            stdout
        )

        return (
            int(failed_match.group(1))
            if failed_match
            else 0
        )

    def _parse_coverage(
        self,
        stdout: str
    ) -> str:
        """
        Parse coverage percentage.
        """

        coverage_match = re.search(

            r"TOTAL\s+\d+\s+\d+\s+(\d+)%",

            stdout
        )

        if coverage_match:

            return (
                coverage_match.group(1)
                + "%"
            )

        return "N/A"