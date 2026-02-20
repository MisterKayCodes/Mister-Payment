import datetime
import uuid
from data.json_storage import read_json, write_json, append_record
from core.config import config
from core.enums import PaymentStatus

# ---------- Payment Methods ----------

async def list_active_payment_methods():
    """
    Return all active payment methods from JSON storage.
    """
    methods = await read_json(config.PAYMENT_METHODS_FILE)
    return [m for m in methods if m.get("is_active", False)]

async def get_active_currencies():
    """
    Returns all unique active currencies dynamically.
    """
    methods = await list_active_payment_methods()
    return sorted({m['currency'] for m in methods})

# ---------- Payment Requests ----------

async def create_payment_request(user_id: int, username: str, currency: str, screenshot_path: str):
    """
    Create a new payment request record asynchronously.
    """
    request = {
        "id": f"req_{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "username": username,
        "currency": currency,
        "screenshot_path": screenshot_path,
        "status": PaymentStatus.PENDING.value,
        "admin_id": None,
        "created_at": datetime.datetime.now(datetime.UTC).isoformat()
    }
    await append_record(config.PAYMENT_REQUESTS_FILE, request)
    return request

async def get_user_payment_status(user_id: int):
    """
    Return the latest payment request for a user.
    """
    requests = await read_json(config.PAYMENT_REQUESTS_FILE)
    user_requests = [r for r in requests if r['user_id'] == user_id]
    
    if not user_requests:
        return None
    
    # Sort by created_at descending (latest first)
    user_requests.sort(key=lambda r: r['created_at'], reverse=True)
    return user_requests[0]