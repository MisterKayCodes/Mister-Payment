import os
import json
import datetime
import uuid
from core.config import config

# ---------- Internal Helpers ----------

async def _local_read(file_path):
    if not os.path.exists(file_path):
        return [] if "methods" in file_path or "requests" in file_path else {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return [] if "methods" in file_path or "requests" in file_path else {}

async def _local_write(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------- Payment Method Management ----------

# UPDATED: Added 'amount' parameter
async def add_payment_method(owner_id: int, currency: str, label: str, name: str, address: str, amount: str, is_active=True):
    """Saves the payment method including the specific price/amount."""
    methods = await _local_read(config.PAYMENT_METHODS_FILE)
    
    method = {
        "id": str(uuid.uuid4().hex[:8]),
        "owner_id": owner_id,
        "currency": currency.upper(),
        "label": label,
        "name": name,
        "address": address,
        "amount": amount,      # <--- NEW FIELD SAVED HERE
        "is_active": is_active,
        "created_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "updated_at": datetime.datetime.now(datetime.UTC).isoformat()
    }
    
    methods.append(method)
    await _local_write(config.PAYMENT_METHODS_FILE, methods)
    return method

async def edit_payment_method(method_id: str, field: str, value: str):
    methods = await _local_read(config.PAYMENT_METHODS_FILE)
    updated = False
    
    for m in methods:
        if m["id"] == method_id:
            if field in m:
                if field == "is_active":
                    value = str(value).lower() == "true"
                m[field] = value
                m["updated_at"] = datetime.datetime.now(datetime.UTC).isoformat()
                updated = True
                break
                
    if updated:
        await _local_write(config.PAYMENT_METHODS_FILE, methods)
    return updated

async def delete_payment_method(method_id: str):
    methods = await _local_read(config.PAYMENT_METHODS_FILE)
    new_methods = [m for m in methods if m["id"] != method_id]
    if len(methods) != len(new_methods):
        await _local_write(config.PAYMENT_METHODS_FILE, new_methods)
        return True
    return False

async def list_payment_methods():
    return await _local_read(config.PAYMENT_METHODS_FILE)

# ---------- Bot Configuration Management ----------

async def get_bot_config():
    config_data = await _local_read(config.BOT_CONFIG_FILE)
    return config_data if isinstance(config_data, dict) else {}

async def update_bot_config(**updates):
    cfg = await get_bot_config()
    cfg.update(updates)
    await _local_write(config.BOT_CONFIG_FILE, cfg)
    return cfg

async def set_admin_contact(username: str, user_id: int):
    return await update_bot_config(admin_contact_username=username, admin_user_id=user_id)

async def register_vault_code(admin_id: int, vault_code: str):
    data = await get_bot_config()
    if "vaults" not in data:
        data["vaults"] = {}
    code = vault_code.upper().strip()
    data["vaults"][code] = admin_id
    await _local_write(config.BOT_CONFIG_FILE, data)
    return True

async def get_admin_id_by_code(vault_code: str):
    data = await get_bot_config()
    return data.get("vaults", {}).get(vault_code.upper())

async def bind_user_to_admin(user_id: int, admin_id: int):
    data = await get_bot_config()
    if "user_bindings" not in data:
        data["user_bindings"] = {}
    data["user_bindings"][str(user_id)] = admin_id
    await _local_write(config.BOT_CONFIG_FILE, data)

async def get_user_assigned_admin(user_id: int):
    data = await get_bot_config()
    return data.get("user_bindings", {}).get(str(user_id))