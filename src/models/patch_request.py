# src/models/patch_request.py
from pydantic import BaseModel
from typing import Optional


class PatchRequest(BaseModel):
    assertion_message: str
    test_name: str
    file_path: str
    error_type: str
    stack_trace: Optional[str] = ""
    line_number: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "assertion_message": "AssertionError: Expected status code 200 but got 500",
                "test_name": "test_login_api",
                "file_path": "tests/test_auth.py",
                "error_type": "AssertionError",
                "stack_trace": "",
                "line_number": 42
            }
        }