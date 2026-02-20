import datetime
import uuid
from data.json_storage import read_json, write_json, append_record
from core.config import config

# ---------- Payment Method Management ----------

def add_payment_method(currency: str, label: str, account_name: str, account_address: str, is_active=True):
    method = {
        "id": str(uuid.uuid4().hex[:8]),
        "currency": currency.upper(),
        "label": label,
        "account_name": account_name,
        "account_address": account_address,
        "is_active": is_active,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat()
    }
    append_record(config.PAYMENT_METHODS_FILE, method)
    return method

def edit_payment_method(method_id: str, **updates):
    methods = read_json(config.PAYMENT_METHODS_FILE)
    updated = False
    for m in methods:
        if m["id"] == method_id:
            for k, v in updates.items():
                if k in m:
                    m[k] = v
            m["updated_at"] = datetime.datetime.utcnow().isoformat()
            updated = True
            break
    if updated:
        write_json(config.PAYMENT_METHODS_FILE, methods)
    return updated

def delete_payment_method(method_id: str):
    methods = read_json(config.PAYMENT_METHODS_FILE)
    new_methods = [m for m in methods if m["id"] != method_id]
    write_json(config.PAYMENT_METHODS_FILE, new_methods)
    return len(methods) != len(new_methods)

def list_payment_methods():
    return read_json(config.PAYMENT_METHODS_FILE)

# ---------- Bot Configuration Management ----------

def get_bot_config():
    config_data = read_json(config.BOT_CONFIG_FILE)
    return config_data

def update_bot_config(**updates):
    cfg = read_json(config.BOT_CONFIG_FILE)
    cfg.update(updates)
    write_json(config.BOT_CONFIG_FILE, cfg)
    return cfg

def set_admin_contact(username: str, user_id: int):
    """
    Dynamically update admin contact.
    """
    return update_bot_config(admin_contact_username=username, admin_user_id=user_id)