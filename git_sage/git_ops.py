import subprocess


def get_staged_diff() -> str:
    return subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True, text=True,
    ).stdout.strip()


def get_staged_files() -> list[str]:
    return [
        f.strip()
        for f in subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            capture_output=True, text=True,
        ).stdout.splitlines()
        if f.strip()
    ]


def create_commit(message: str) -> bool:
    return subprocess.run(["git", "commit", "-m", message]).returncode == 0
