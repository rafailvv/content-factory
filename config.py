import os

from dotenv import load_dotenv

class Config:
    def __init__(self, env_path = ".env"):
        load_dotenv(env_path)

        self.api_id = os.getenv("API_ID")
        self.api_hash = os.getenv("API_HASH")
        self.session_name=os.getenv("SESSION_NAME")
        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

        self.source_channels = ["mosguru", "moscowmap", "msk_live"]
