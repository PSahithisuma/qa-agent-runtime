import re


def parse_failures(stdout: str):

    failures = []

    pattern = re.finditer(

        r"_{5,}\s(.+?)\s_{5,}.*?"
        r"E\s+(.+?)\n.*?"
        r"(.+?):(\d+):",

        stdout,

        re.DOTALL
    )

    for match in pattern:

        test_name = match.group(1).strip()

        assertion = match.group(2).strip()

        file_path = match.group(3).strip()

        line_number = int(match.group(4))

        failures.append({

            "test_name": test_name,

            "assertion_message": assertion,

            "file_path": file_path,

            "line_number": line_number,

            "error_type": "AssertionError"
        })

    return failures
