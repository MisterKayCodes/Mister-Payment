import json
from typing import List, Dict, Any

def read_json(path: str) -> List[Dict[str, Any]]:
    """
    Load JSON file. Returns empty list if file doesn't exist.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def write_json(path: str, data: List[Dict[str, Any]]) -> None:
    """
    Overwrite JSON file with new data.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def append_record(path: str, record: Dict[str, Any]) -> None:
    """
    Append a single record to JSON file.
    """
    data = read_json(path)
    data.append(record)
    write_json(path, data)

def update_record(path: str, record_id: str, updates: Dict[str, Any]) -> bool:
    """
    Update a record by id. Returns True if updated.
    """
    data = read_json(path)
    updated = False
    for item in data:
        if item.get("id") == record_id:
            item.update(updates)
            updated = True
            break
    if updated:
        write_json(path, data)
    return updated