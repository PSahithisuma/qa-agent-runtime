# tests/test_sandbox.py
from src.sandbox.docker_sandbox import DockerSandbox
from src.runner.test_runner import TestRunner
import os

def test_docker_available():
    sandbox = DockerSandbox()
    available = sandbox.is_available()
    print(f"Docker available: {available}")
    assert True  # just check it initializes

def test_framework_detection():
    runner = TestRunner()
    # Test on current directory
    framework = runner.detect_framework(".")
    print(f"Detected framework: {framework}")
    assert framework is not None

def test_runner_bad_path():
    runner = TestRunner()
    result = runner.run("/nonexistent/path")
    assert result["success"] == False
    assert "not found" in result["error"]
print("watcher test")