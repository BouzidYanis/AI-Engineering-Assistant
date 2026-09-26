"""Search the local migration guide."""

import re
from mcp_server.tools.files import read_project_file


def search_documentation(query: str) -> str:
    """Return guide paragraphs containing any query word of at least 3 characters."""
    words = [word.casefold() for word in query.split() if len(word) > 2]
    content = read_project_file("data/migration_guide.txt")
    matches = [
        paragraph.strip() for paragraph in re.split(r"\n\s*\n", content)
        if any(word in paragraph.casefold() for word in words)
    ]
    return "\n\n".join(matches) or "No relevant documentation found."
