"""Read evidence independently of the working directory."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "data"


def resolve_data_path(file_path: str) -> Path:
    """Accept project-relative or absolute paths restricted to data/."""
    path = Path(file_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path = path.resolve()
    if not path.is_relative_to(DATA_ROOT.resolve()):
        raise ValueError("Access is restricted to the project's data directory.")
    return path


def list_project_files(directory: str = "data") -> str:
    """List evidence under data/ using project-relative paths."""
    path = resolve_data_path(directory)
    if not path.is_dir():
        raise ValueError(f"Not a directory: {directory}")
    files = sorted(
        str(file.relative_to(PROJECT_ROOT))
        for file in path.rglob("*")
        if file.is_file() and file.resolve().is_relative_to(DATA_ROOT.resolve())
    )
    return "\n".join(files) or "No files found."


def read_project_file(file_path: str) -> str:
    """Read a UTF-8 evidence file under data/."""
    return resolve_data_path(file_path).read_text(encoding="utf-8")
