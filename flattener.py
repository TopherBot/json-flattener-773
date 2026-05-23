#!/usr/bin/env python3
"""json-flattener – flatten/unflatten JSON to dot‑notation.

Features:
* Read from stdin, a file, or a URL.
* Flatten nested objects (dicts & lists) into dot‑notation keys.
* Optional unflatten mode.
* Colour‑coded output (keys in cyan, values type‑aware).
"""

import argparse, json, sys, urllib.request, pathlib
from typing import Any, Dict

# ---------- colour helpers ----------
RESET = "\033[0m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"

def color_key(k: str) -> str:
    return f"{CYAN}{k}{RESET}"

def color_value(v: Any) -> str:
    if isinstance(v, str):
        return f"{YELLOW}\"{v}\"{RESET}"
    if isinstance(v, bool):
        return f"{GREEN}{v}{RESET}"
    if v is None:
        return f"{RED}null{RESET}"
    return f"{v}"

# ---------- flatten / unflatten ----------
def _flatten(obj: Any, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    items: Dict[str, Any] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.update(_flatten(v, new_key, sep=sep))
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            new_key = f"{parent_key}{sep}{idx}" if parent_key else str(idx)
            items.update(_flatten(v, new_key, sep=sep))
    else:
        items[parent_key] = obj
    return items

def flatten(data: Any) -> Dict[str, Any]:
    return _flatten(data)

def _unflatten(pairs: Dict[str, Any], sep: str = ".") -> Any:
    root: Any = {}
    for flat_key, value in pairs.items():
        parts = flat_key.split(sep)
        cur = root
        for i, part in enumerate(parts):
            # decide if next container is a list or dict
            is_last = i == len(parts) - 1
            try:
                idx = int(part)
                is_index = True
            except ValueError:
                is_index = False
            if is_index:
                if not isinstance(cur, list):
                    cur_parent = cur
                    cur = []
                    # attach to parent correctly
                    if isinstance(cur_parent, dict):
                        cur_parent[parts[i-1]] = cur
                # extend list size
                while len(cur) <= idx:
                    cur.append({})
                if is_last:
                    cur[idx] = value
                else:
                    if not isinstance(cur[idx], (list, dict)):
                        cur[idx] = {}
                    cur = cur[idx]
            else:
                if not isinstance(cur, dict):
                    cur_parent = cur
                    cur = {}
                    if isinstance(cur_parent, list):
                        cur_parent[int(parts[i-1])] = cur
                if is_last:
                    cur[part] = value
                else:
                    cur = cur.setdefault(part, {})
    return root

def unflatten(pairs: Dict[str, Any]) -> Any:
    return _unflatten(pairs)

# ---------- I/O helpers ----------
def load_json(source: str) -> Any:
    if source == "-":
        return json.load(sys.stdin)
    if source.startswith("http://") or source.startswith("https://"):
        with urllib.request.urlopen(source) as resp:
            return json.load(resp)
    path = pathlib.Path(source)
    with path.open() as f:
        return json.load(f)

def dump_flat(pairs: Dict[str, Any]) -> None:
    for k in sorted(pairs):
        print(f"{color_key(k)}: {color_value(pairs[k])}")

# ---------- CLI ----------
def main() -> None:
    parser = argparse.ArgumentParser(description="Flatten or unflatten JSON to dot‑notation.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="Path to a JSON file (use - for stdin)")
    group.add_argument("-u", "--url", help="URL returning JSON")
    parser.add_argument("--unflatten", action="store_true", help="Treat input as flattened key/value map and rebuild original JSON")
    args = parser.parse_args()

    src = args.file if args.file is not None else args.url
    data = load_json(src)
    if args.unflatten:
        if not isinstance(data, dict):
            sys.exit("Error: unflatten mode expects a JSON object of flat key/value pairs.")
        rebuilt = unflatten(data)
        json.dump(rebuilt, sys.stdout, indent=2)
        print()
    else:
        flat = flatten(data)
        dump_flat(flat)

if __name__ == "__main__":
    main()
