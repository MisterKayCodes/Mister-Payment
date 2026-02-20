import datetime
import uuid
from data.json_storage import read_json, write_json, append_record
from core.config import config

# ---------- Payment Method Management ----------

async def add_payment_method(currency: str, label: str, account_name: str, account_address: str, is_active=True):
    method = {
        "id": str(uuid.uuid4().hex[:8]),
        "currency": currency.upper(),
        "label": label,
        "account_name": account_name,
        "account_address": account_address,
        "is_active": is_active,
        # Modern way to get UTC time in 2026
        "created_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "updated_at": datetime.datetime.now(datetime.UTC).isoformat()
    }
    await append_record(config.PAYMENT_METHODS_FILE, method)
    return method

async def edit_payment_method(method_id: str, **updates):
    methods = await read_json(config.PAYMENT_METHODS_FILE)
    updated = False
    for m in methods:
        if m["id"] == method_id:
            for k, v in updates.items():
                if k in m:
                    m[k] = v
            m["updated_at"] = datetime.datetime.now(datetime.UTC).isoformat()
            updated = True
            break
    if updated:
        await write_json(config.PAYMENT_METHODS_FILE, methods)
    return updated

async def delete_payment_method(method_id: str):
    methods = await read_json(config.PAYMENT_METHODS_FILE)
    new_methods = [m for m in methods if m["id"] != method_id]
    if len(methods) != len(new_methods):
        await write_json(config.PAYMENT_METHODS_FILE, new_methods)
        return True
    return False

async def list_payment_methods():
    return await read_json(config.PAYMENT_METHODS_FILE)

# ---------- Bot Configuration Management ----------

async def get_bot_config():
    # Since this might return a dict or list, handle default empty dict
    config_data = await read_json(config.BOT_CONFIG_FILE)
    return config_data if config_data else {}

async def update_bot_config(**updates):
    cfg = await get_bot_config()
    cfg.update(updates)
    await write_json(config.BOT_CONFIG_FILE, cfg)
    return cfg

async def set_admin_contact(username: str, user_id: int):
    """
    Dynamically update admin contact.
    """
    return await update_bot_config(admin_contact_username=username, admin_user_id=user_id)