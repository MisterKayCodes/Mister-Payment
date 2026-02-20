from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"

class CallbackActions(str, Enum):
    APPROVE = "approve"
    DECLINE = "decline"