# src/formatter/output_formatter.py

import os
import re
from datetime import datetime

from rich.console import Console
from rich.table import Table

from src.formatter.error_analyzer import analyze_error

console = Console()


def extract_coverage(stdout):

    match = re.search(
        r"TOTAL\s+\d+\s+\d+\s+(\d+)%",
        stdout
    )

    if match:
        return match.group(1) + "%"

    return "N/A"


def save_logs(result):

    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    log_file = f"logs/run_{timestamp}.txt"

    with open(log_file, "w", encoding="utf-8") as f:

        f.write("QA PIPELINE RESULTS\n\n")

        for key, value in result.items():

            f.write(f"{key}: {value}\n\n")

    return log_file


def print_results(result):

    console.rule(
        "[bold blue]QA Pipeline Results[/bold blue]"
    )

    coverage = extract_coverage(
        result.get("stdout", "")
    )

    table = Table(
        show_header=True,
        header_style="bold magenta"
    )

    table.add_column("Metric")
    table.add_column("Value")

    table.add_row(
        "Success",
        str(result.get("success"))
    )

    table.add_row(
        "Framework",
        result.get("framework_detected", "N/A")
    )

    table.add_row(
        "Total Tests",
        str(result.get("total_tests", 0))
    )

    table.add_row(
        "Passed",
        str(result.get("passed_tests", 0))
    )

    table.add_row(
        "Failed",
        str(result.get("failed_tests", 0))
    )

    table.add_row(
        "Coverage",
        coverage
    )

    table.add_row(
        "Exit Code",
        str(result.get("exit_code", -1))
    )

    console.print(table)

    if result.get("success"):

        console.print(
            "\n[green]All tests passed[/green]"
        )

    else:

        console.print(
            "\n[red]Some tests failed[/red]"
        )

    console.print(
        "\n[cyan]Test Output:[/cyan]\n"
    )

    console.print(
        result.get("stdout", "")
    )

    if result.get("stderr"):

        console.print(
            "\n[red]Errors:[/red]\n"
        )

        console.print(
            result.get("stderr", "")
        )

    if not result.get("success"):

        suggestion = analyze_error(
            result.get("stdout", "") +
            result.get("stderr", "")
        )

        console.print(
            "\n[yellow]Suggested Fix:[/yellow]\n"
        )

        for fix in suggestion:

         console.print(
        f"[yellow]- {fix}[/yellow]"
    )

    # Save logs
    log_file = save_logs(result)

    console.print(
        f"\n[green]Logs saved:[/green] {log_file}"
    )