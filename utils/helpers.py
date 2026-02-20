import datetime
import uuid

def timestamp_utc() -> str:
    """
    Returns current UTC timestamp as ISO string using modern standards.
    """
    # datetime.datetime.utcnow() is deprecated in newer Python versions
    return datetime.datetime.now(datetime.UTC).isoformat()

def generate_id(prefix: str = "id") -> str:
    """
    Generate a short unique ID with optional prefix.
    """
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def format_currency(amount: float, currency: str) -> str:
    """
    Simple currency formatting (e.g., USD 1,250.50).
    """
    return f"{currency.upper()} {amount:,.2f}"