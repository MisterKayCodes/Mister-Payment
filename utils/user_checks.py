from data.json_storage import read_json
from core.config import config
from core.enums import PaymentStatus

async def has_pending_request(user_id: int) -> bool:
    """
    Checks if a specific user has any request with a 'pending' status.
    """
    requests = await read_json(config.PAYMENT_REQUESTS_FILE)
    if not isinstance(requests, list):
        return False
        
    # Look for any record matching the user_id and PENDING status
    for r in requests:
        if r.get('user_id') == user_id and r.get('status') == PaymentStatus.PENDING.value:
            return True
    return False