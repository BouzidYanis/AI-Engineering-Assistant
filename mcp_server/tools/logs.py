"""Application log diagnostics."""

import re
from mcp_server.tools.files import read_project_file


def analyze_logs(log_file: str) -> str:
    """Return warning and error lines from a log file under data/."""
    problems = [
        line for line in read_project_file(log_file).splitlines()
        if re.search(r"\b(?:WARNING|ERROR)\b", line, re.IGNORECASE)
    ]
    return "\n".join(problems) or "No warnings or errors found in the log file."
