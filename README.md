# Mister Payment Bot

A simple Telegram bot for handling payment confirmations.  
Dynamic, admin-controlled, and fully reusable for any service you sell (ghostwriting, APIs, signals, etc.).

---

## Features

- Users select a payment currency (dynamic, admin can add new ones)
- Admin sets payment methods (bank, crypto, mobile money, etc.)
- Users upload payment screenshots
- Admin approves or declines payments
- Users can check status or contact admin if delayed
- Fully dynamic and JSON-based storage
- Logs every action for easy debugging

---

## Setup

1. Clone the repo:

```bash
git clone <your-repo-url>
cd mister_payment
````

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file (see `.env.example`):

```
BOT_TOKEN=your_bot_token_here
ADMIN_USER_ID=123456789
STORAGE_DIR=storage
LOG_DIR=logs
MAX_FILE_SIZE_MB=5
```

5. Run the bot:

```bash
python main.py
```

---

## Folder Structure

```
mister_payment/
├── bot/
│   ├── handlers/
│   └── keyboards/
├── core/
├── data/
├── services/
├── utils/
├── storage/
├── logs/
├── main.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

## Notes

* Admin can dynamically add new payment methods and currencies.
* JSON files act as lightweight database (payment_methods.json, payment_requests.json, bot_config.json).
* Fully compatible with Aiogram v3 and Ubuntu VPS.

---

❤️ From Mister
