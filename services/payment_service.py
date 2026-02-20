import datetime
import uuid
from data.json_storage import read_json, write_json, append_record
from core.config import config
from core.enums import PaymentStatus

def list_active_payment_methods():
    """
    Return all active payment methods from JSON storage.
    """
    methods = read_json(config.PAYMENT_METHODS_FILE)
    return [m for m in methods if m.get("is_active", False)]

def get_active_currencies():
    """
    Returns all unique active currencies dynamically.
    """
    methods = list_active_payment_methods()
    return sorted({m['currency'] for m in methods})

def create_payment_request(user_id: int, username: str, currency: str, screenshot_path: str):
    """
    Create a new payment request record.
    """
    request = {
        "id": f"req_{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "username": username,
        "currency": currency,
        "screenshot_path": screenshot_path,
        "status": PaymentStatus.PENDING.value,
        "admin_id": None,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    append_record(config.PAYMENT_REQUESTS_FILE, request)
    return request

def get_user_payment_status(user_id: int):
    """
    Return the latest payment request for a user.
    """
    requests = read_json(config.PAYMENT_REQUESTS_FILE)
    user_requests = [r for r in requests if r['user_id'] == user_id]
    if not user_requests:
        return None
    # Return latest request
    user_requests.sort(key=lambda r: r['created_at'], reverse=True)
    return user_requests[0]