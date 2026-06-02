import os
import sys
import tempfile
import subprocess

import click

from .ai import generate_message
from .git_ops import create_commit, get_staged_diff, get_staged_files


@click.command()
@click.option("--commit", "-c", is_flag=True, help="Commit immediately with the generated message")
@click.option("--edit", "-e", is_flag=True, help="Open message in $EDITOR before committing")
def main(commit, edit):
    """Generate an AI commit message from your staged changes.

    \b
    Examples:
      git add -A && git-sage
      git-sage --commit
      git-sage --edit --commit
    """
    diff = get_staged_diff()
    files = get_staged_files()

    if not diff:
        click.echo("No staged changes. Run `git add` first.", err=True)
        sys.exit(1)

    click.echo("Generating commit message...", err=True)

    try:
        message = generate_message(diff, files)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if edit:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(message)
            tmp = f.name
        editor = os.environ.get("EDITOR", "vi")
        subprocess.run([editor, tmp])
        message = open(tmp).read().strip()
        os.unlink(tmp)

    click.echo(f"\n{message}\n")

    if commit:
        if create_commit(message):
            click.echo("✓ Committed.", err=True)
        else:
            sys.exit(1)
    else:
        click.echo("Tip: run with --commit to use this message directly.", err=True)
