import datetime
from data.json_storage import read_json, write_json
from core.config import config
from core.enums import PaymentStatus

async def update_payment_status(request_id: str, admin_id: int, approve: bool):
    """
    Update a payment request to approved or declined asynchronously.
    """
    requests = await read_json(config.PAYMENT_REQUESTS_FILE)
    updated = False
    
    for r in requests:
        if r["id"] == request_id:
            r["status"] = PaymentStatus.APPROVED.value if approve else PaymentStatus.DECLINED.value
            r["admin_id"] = admin_id
            # Using modern UTC timing for 2026
            r["updated_at"] = datetime.datetime.now(datetime.UTC).isoformat()
            updated = True
            break
            
    if updated:
        await write_json(config.PAYMENT_REQUESTS_FILE, requests)
    return updated

async def get_pending_requests():
    """
    Return all pending payment requests for admin review.
    """
    requests = await read_json(config.PAYMENT_REQUESTS_FILE)
    return [r for r in requests if r["status"] == PaymentStatus.PENDING.value]