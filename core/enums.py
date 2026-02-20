from enum import Enum
from aiogram.filters.callback_data import CallbackData

class PaymentStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"

class CallbackActions(str, Enum):
    APPROVE = "approve"
    DECLINE = "decline"

# NEW: The v3 Callback Data Factory
# This makes handling admin button clicks 100x easier
class PaymentReviewCallback(CallbackData, prefix="pay_rev"):
    action: CallbackActions
    request_id: str