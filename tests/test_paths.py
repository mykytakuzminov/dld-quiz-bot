from pathlib import Path

import pytest

from dld_quiz_bot.paths import find_project_root


def test_find_project_root():
    root = find_project_root()

    assert root.exists()
    assert (root / "pyproject.toml").exists()
    assert root.is_dir()


def test_find_projet_root_raise_error():
    fake_path = Path("/nonexistent/deep/folder/file.py")

    with pytest.raises(FileNotFoundError):
        find_project_root(fake_path)
