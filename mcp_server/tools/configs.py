"""JSON configuration comparisons."""

import json
from mcp_server.tools.files import read_project_file


def compare_configs(old_config: str, new_config: str) -> str:
    """Compare top-level JSON keys; changed nested objects appear as whole values."""
    old = json.loads(read_project_file(old_config))
    new = json.loads(read_project_file(new_config))
    if not isinstance(old, dict) or not isinstance(new, dict):
        raise ValueError("Configurations must be JSON objects.")
    return json.dumps({
        "removed": {key: old[key] for key in old if key not in new},
        "added": {key: new[key] for key in new if key not in old},
        "modified": {
            key: {"old": old[key], "new": new[key]}
            for key in old if key in new and old[key] != new[key]
        },
    }, indent=2, ensure_ascii=False)
