import os
import json
import datetime
import uuid
from core.config import config
from core.enums import PaymentStatus

# ---------- Helper to replace broken json_storage ----------
async def _local_read_json(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

async def _local_append_record(file_path, record):
    data = await _local_read_json(file_path)
    data.append(record)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------- Payment Methods ----------

async def list_active_payment_methods():
    """Return all active payment methods."""
    methods = await _local_read_json(config.PAYMENT_METHODS_FILE)
    if not isinstance(methods, list):
        return []
    return [m for m in methods if m.get("is_active", True)]

async def get_active_currencies(owner_id: int = None):
    """Fetches active payment methods filtered by Vault owner."""
    all_methods = await _local_read_json(config.PAYMENT_METHODS_FILE)
    
    # 1. Filter by Active status
    active_methods = [m for m in all_methods if m.get("is_active", True)]
    
    # 2. Filter by Owner (The Vault Persona)
    if owner_id:
        active_methods = [
            m for m in active_methods 
            if str(m.get("owner_id")) == str(owner_id)
        ]
        
    return active_methods

# ---------- Payment Requests ----------

async def create_payment_request(user_id: int, username: str, currency: str, screenshot_path: str, owner_id: int):
    """Create a new payment request record (Linked to Vault Admin)."""
    request = {
        "id": f"req_{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "username": username,
        "currency": currency,
        "screenshot_path": screenshot_path,
        "owner_id": owner_id,  # <--- Added for Vault system
        "status": PaymentStatus.PENDING.value,
        "admin_id": None,
        "created_at": datetime.datetime.now(datetime.UTC).isoformat()
    }
    await _local_append_record(config.PAYMENT_REQUESTS_FILE, request)
    return request

async def get_user_payment_status(user_id: int):
    """Return the latest payment request for a user."""
    requests = await _local_read_json(config.PAYMENT_REQUESTS_FILE)
    if not isinstance(requests, list):
        return None
        
    user_requests = [r for r in requests if r.get('user_id') == user_id]
    
    if not user_requests:
        return None
    
    # Sort by created_at descending (latest first)
    user_requests.sort(key=lambda r: r.get('created_at', ""), reverse=True)
    return user_requests[0]