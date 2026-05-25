# src/fixer/auto_fixer.py

import re


class AutoFixer:

    def suggest_fix(self, output: str):

        fixes = []

        if "ModuleNotFoundError" in output:

            match = re.search(
                r"No module named '(.+?)'",
                output
            )

            if match:

                pkg = match.group(1)

                fixes.append(
                    f"pip install {pkg}"
                )

        if "AssertionError" in output:

            fixes.append(
                "Check assertion expected vs actual values."
            )

        if "ConnectionRefusedError" in output:

            fixes.append(
                "Ensure dependent service is running."
            )

        if not fixes:

            fixes.append(
                "No automatic fix available."
            )

        return fixes