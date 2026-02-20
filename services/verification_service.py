import datetime
from data.json_storage import read_json, write_json
from core.config import config
from core.enums import PaymentStatus

def update_payment_status(request_id: str, admin_id: int, approve: bool):
    """
    Update a payment request to approved or declined.
    """
    requests = read_json(config.PAYMENT_REQUESTS_FILE)
    updated = False
    for r in requests:
        if r["id"] == request_id:
            r["status"] = PaymentStatus.APPROVED.value if approve else PaymentStatus.DECLINED.value
            r["admin_id"] = admin_id
            r["updated_at"] = datetime.datetime.utcnow().isoformat()
            updated = True
            break
    if updated:
        write_json(config.PAYMENT_REQUESTS_FILE, requests)
    return updated

def get_pending_requests():
    """
    Return all pending payment requests for admin review.
    """
    requests = read_json(config.PAYMENT_REQUESTS_FILE)
    return [r for r in requests if r["status"] == PaymentStatus.PENDING.value]