#!/usr/bin/env python3
"""
Scanner for deprecated API calls.
Usage: python scanner.py <file_or_directory>
Output: JSON with list of files and occurrences.
"""

import os
import re
import sys
import json
from pathlib import Path

# Patterns matching regex-patterns.md
PATTERNS = {
    "python": [
        (r"old_api\.get_user\s*\(", "old_api.get_user"),
        (r"old_api\.fetch_posts\s*\(", "old_api.fetch_posts"),
        (r"from\s+old_api\s+import", "import old_api"),
    ],
    "javascript": [
        (r"oldApi\.getUser\s*\(", "oldApi.getUser"),
        (r"oldApi\.fetchPosts\s*\(", "oldApi.fetchPosts"),
        (r"require\s*\(\s*['\"]old-api['\"]\s*\)", "require('old-api')"),
    ],
}

EXTENSION_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
}

def scan_file(file_path):
    import sys
    lang = EXTENSION_MAP.get(file_path.suffix.lower())
    if not lang:
        sys.stderr.write(f"WARNING: Unsupported extension {file_path.suffix} for {file_path}\n")
        return None
    """Scan a single file. Return dict with path and occurrences."""
    lang = EXTENSION_MAP.get(file_path.suffix.lower())
    if not lang:
        return None

    patterns = PATTERNS.get(lang, [])
    if not patterns:
        return None

    occurrences = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return {"path": str(file_path), "error": str(e), "occurrences": []}

    for line_num, line in enumerate(lines, start=1):
        for regex, pattern_name in patterns:
            if re.search(regex, line):
                occurrences.append({
                    "line": line_num,
                    "code": line.rstrip("\n"),
                    "pattern": pattern_name
                })
    return {
        "path": str(file_path),
        "occurrences": occurrences
    }

def scan_directory(root_dir):
    """Recursively scan all supported files."""
    results = []
    root = Path(root_dir)
    for ext in EXTENSION_MAP:
        for file_path in root.rglob(f"*{ext}"):
            res = scan_file(file_path)
            if res and res["occurrences"]:
                results.append(res)
    return results

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No path provided. Usage: scanner.py <path>"}))
        sys.exit(1)

    target = sys.argv[1]
    path = Path(target)

    if not path.exists():
        print(json.dumps({"error": f"Path does not exist: {target}"}))
        sys.exit(1)

    if path.is_file():
        result = scan_file(path)
        if result and result["occurrences"]:
            output = {"files": [result]}
        else:
            output = {"files": []}
    elif path.is_dir():
        results = scan_directory(path)
        output = {"files": results}
    else:
        print(json.dumps({"error": "Path is neither file nor directory"}))
        sys.exit(1)

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
