import typer
from rich.console import Console

from src.runner.test_runner import TestRunner
from src.formatter.output_formatter import print_results
from src.models.test_failure import TestFailure

app = typer.Typer()

console = Console()


@app.command()
def run(path: str = "."):
    """
    Run QA pipeline on a project.
    """

    console.print(
        f"[cyan]Running QA pipeline on:[/cyan] {path}"
    )

    runner = TestRunner()

    result = runner.run(
        codebase_path=path
    )

    if result.get("success", False):

        console.print(
            "[green]Tests completed successfully[/green]"
        )

    else:

        console.print(
            "[red]Tests failed[/red]"
        )

    print_results(result)


@app.command()
def watch():
    """
    Watch files continuously.
    """

    console.print(
        "[yellow]Watcher started...[/yellow]"
    )


if __name__ == "__main__":

    app()