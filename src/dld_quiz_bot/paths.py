from pathlib import Path


def find_project_root() -> Path:
    current = Path(__file__)
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError("pyproject.toml not found")
