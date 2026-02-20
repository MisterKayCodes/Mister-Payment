import os
import json
import datetime
from core.config import config
from core.enums import PaymentStatus

# ---------- Internal Helpers (Replacing broken json_storage) ----------

async def _local_read_list(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

async def _local_write_list(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------- Verification Logic ----------

async def update_payment_status(request_id: str, admin_id: int, approve: bool):
    """
    Update a payment request to approved or declined asynchronously.
    """
    requests = await _local_read_list(config.PAYMENT_REQUESTS_FILE)
    updated = False
    
    for r in requests:
        if r.get("id") == request_id:
            r["status"] = PaymentStatus.APPROVED.value if approve else PaymentStatus.DECLINED.value
            r["admin_id"] = admin_id
            # Using modern UTC timing for 2026
            r["updated_at"] = datetime.datetime.now(datetime.UTC).isoformat()
            updated = True
            break
            
    if updated:
        await _local_write_list(config.PAYMENT_REQUESTS_FILE, requests)
    return updated

async def get_pending_requests():
    """
    Return all pending payment requests for admin review.
    """
    requests = await _local_read_list(config.PAYMENT_REQUESTS_FILE)
    return [r for r in requests if r.get("status") == PaymentStatus.PENDING.value]