# Best Prompt for Mister Payment Project Setup

To get the agent into this state quickly and efficiently (saving tokens and time), use the following prompt:

```markdown
Unzip `attached_assets/Mister-Payment_*.zip`, move all contents to the root folder, and delete the original zip and the empty template files (client/, server/, shared/, etc.). This is a Python Telegram bot project using `aiogram`. Install dependencies from `requirements.txt` using the packager tool. Ensure `python-3.11` is installed. The bot uses `BOT_TOKEN` and `ADMIN_USER_ID` from environment variables/secrets. Run `python main.py` to verify the setup.
```

## Key Instructions Included:
1. **File Management**: Direct instructions to move files to root and cleanup templates.
2. **Tech Stack**: Explicitly mentions Python, `aiogram`, and version 3.11.
3. **Dependencies**: Points directly to `requirements.txt`.
4. **Environment**: Identifies the necessary secrets/env vars.
5. **Execution**: Provides the entry point command.
