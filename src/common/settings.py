import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    agentverse_token: str = os.getenv("AGENTVERSE_TOKEN", "")
    mailbox_secret: str = os.getenv("MAILBOX_SECRET", "")
    asi_one_api_key: str = os.getenv("ASI_ONE_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    claude_api_key: str = os.getenv("CLAUDE_API_KEY", "")


settings = Settings()
