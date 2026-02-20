from dataclasses import dataclass, field
from typing import Optional

@dataclass
class PaymentMethod:
    id: str
    currency: str
    label: str
    account_name: str
    account_address: str
    is_active: bool = True
    created_at: str = ""
    updated_at: str = ""

@dataclass
class PaymentRequest:
    id: str
    user_id: int
    username: str
    currency: str
    screenshot_path: str
    status: str
    admin_id: Optional[int] = None
    created_at: str = ""
    updated_at: str = ""

@dataclass
class BotConfig:
    admin_contact_username: str
    admin_user_id: int
    verification_note: str = "Verification may take some time."
    auto_reply_message: str = "Your payment is being reviewed."