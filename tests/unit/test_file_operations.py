"""Tests for file operations tool."""

import pytest
from pathlib import Path
from src.dev_tools.file_operations import (
    read_file,
    write_file,
    list_files,
    delete_file,
)


def test_write_and_read_file(tmp_path: Path) -> None:
    """Test writing and reading a file."""
    test_file = tmp_path / "test.txt"
    content = "Hello, World!"

    result = write_file(str(test_file), content)
    assert "13 characters" in result

    read_content = read_file(str(test_file))
    assert read_content == content


def test_read_file_with_line_range(tmp_path: Path) -> None:
    """Test reading specific lines from a file."""
    test_file = tmp_path / "lines.txt"
    content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
    write_file(str(test_file), content)

    result = read_file(str(test_file), start_line=2, end_line=4)
    assert result == "Line 2\nLine 3\nLine 4"


def test_read_file_not_found() -> None:
    """Test reading nonexistent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_file("/nonexistent/file.txt")


def test_read_file_invalid_line_numbers(tmp_path: Path) -> None:
    """Test invalid line numbers raise ValueError."""
    test_file = tmp_path / "test.txt"
    write_file(str(test_file), "Line 1\nLine 2")

    with pytest.raises(ValueError):
        read_file(str(test_file), start_line=0, end_line=1)

    with pytest.raises(ValueError):
        read_file(str(test_file), start_line=2, end_line=1)


def test_list_files(tmp_path: Path) -> None:
    """Test listing files in a directory."""
    (tmp_path / "file1.txt").touch()
    (tmp_path / "file2.py").touch()
    (tmp_path / "subdir").mkdir()

    all_files = list_files(str(tmp_path))
    assert len(all_files) == 2
    assert "file1.txt" in all_files
    assert "file2.py" in all_files


def test_list_files_with_pattern(tmp_path: Path) -> None:
    """Test listing files with glob pattern."""
    (tmp_path / "test1.py").touch()
    (tmp_path / "test2.py").touch()
    (tmp_path / "readme.txt").touch()

    py_files = list_files(str(tmp_path), pattern="*.py")
    assert len(py_files) == 2
    assert all(f.endswith(".py") for f in py_files)


def test_list_files_recursive(tmp_path: Path) -> None:
    """Test recursive file listing."""
    (tmp_path / "file1.txt").touch()
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file2.txt").touch()

    all_files = list_files(str(tmp_path), recursive=True)
    assert len(all_files) == 2
    assert "file1.txt" in all_files
    assert "subdir/file2.txt" in all_files


def test_list_files_not_found() -> None:
    """Test listing nonexistent directory raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        list_files("/nonexistent/directory")


def test_delete_file(tmp_path: Path) -> None:
    """Test deleting a file."""
    test_file = tmp_path / "delete_me.txt"
    test_file.touch()

    result = delete_file(str(test_file))
    assert "Deleted" in result
    assert not test_file.exists()


def test_delete_file_not_found() -> None:
    """Test deleting nonexistent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        delete_file("/nonexistent/file.txt")


def test_write_file_creates_directories(tmp_path: Path) -> None:
    """Test that write_file creates parent directories."""
    test_file = tmp_path / "nested" / "dir" / "file.txt"
    content = "Test"

    write_file(str(test_file), content, create_dirs=True)
    assert test_file.exists()
    assert test_file.read_text() == content
