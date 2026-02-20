import json
import aiofiles
import os
from typing import List, Dict, Any

async def read_json(path: str) -> List[Dict[str, Any]]:
    """
    Load JSON file asynchronously.
    """
    if not os.path.exists(path):
        return []
    try:
        async with aiofiles.open(path, mode="r", encoding="utf-8") as f:
            contents = await f.read()
            return json.loads(contents)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

async def write_json(path: str, data: List[Dict[str, Any]]) -> None:
    """
    Overwrite JSON file asynchronously.
    """
    async with aiofiles.open(path, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(data, indent=4))

async def append_record(path: str, record: Dict[str, Any]) -> None:
    """
    Append a single record asynchronously.
    """
    data = await read_json(path)
    data.append(record)
    await write_json(path, data)

async def update_record(path: str, record_id: str, updates: Dict[str, Any]) -> bool:
    """
    Update a record by id asynchronously.
    """
    data = await read_json(path)
    updated = False
    for item in data:
        if str(item.get("id")) == str(record_id): # String conversion for safety
            item.update(updates)
            updated = True
            break
    if updated:
        await write_json(path, data)
    return updated