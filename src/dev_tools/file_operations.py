"""File operations tool for Letta development agents."""

from pathlib import Path
from typing import List, Optional


def read_file(
    file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None
) -> str:
    """
    Read contents of a file.

    Args:
        file_path: Absolute path to the file
        start_line: Optional starting line (1-indexed)
        end_line: Optional ending line (inclusive, 1-indexed)

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If line numbers are invalid
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    content = path.read_text()

    if start_line is not None and end_line is not None:
        lines = content.splitlines()

        if start_line < 1 or end_line < 1:
            raise ValueError("Line numbers must be >= 1")
        if start_line > end_line:
            raise ValueError(f"start_line ({start_line}) > end_line ({end_line})")
        if start_line > len(lines):
            raise ValueError(f"start_line ({start_line}) exceeds file length ({len(lines)})")

        return "\n".join(lines[start_line - 1 : end_line])

    return content


def write_file(file_path: str, content: str, create_dirs: bool = True) -> str:
    """
    Write content to a file.

    Args:
        file_path: Absolute path to file
        content: Content to write
        create_dirs: Create parent directories if they don't exist

    Returns:
        Success message with file path and character count

    Raises:
        PermissionError: If lacking write permissions
        OSError: If file system operation fails
    """
    path = Path(file_path)

    if create_dirs:
        path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content)
    return f"Wrote {len(content)} characters to {file_path}"


def list_files(directory: str, pattern: str = "*", recursive: bool = False) -> List[str]:
    """
    List files in a directory.

    Args:
        directory: Path to directory
        pattern: Glob pattern (e.g., "*.py", "test_*")
        recursive: Search recursively if True

    Returns:
        List of file paths (relative to directory)

    Raises:
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    path = Path(directory)

    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    if recursive:
        files = path.rglob(pattern)
    else:
        files = path.glob(pattern)

    # Return only files, not directories, as relative paths
    return [str(f.relative_to(path)) for f in files if f.is_file()]


def delete_file(file_path: str) -> str:
    """
    Delete a file.

    Args:
        file_path: Path to file to delete

    Returns:
        Success message

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If lacking permissions
        IsADirectoryError: If path is a directory
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.is_dir():
        raise IsADirectoryError(f"Cannot delete directory with delete_file: {file_path}")

    path.unlink()
    return f"Deleted {file_path}"
