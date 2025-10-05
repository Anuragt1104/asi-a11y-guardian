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
    orchestrator_addr: str = os.getenv("ORCHESTRATOR_ADDR", "")
    orch_fetcher_addr: str = os.getenv("ORCH_FETCHER_ADDR", "")
    orch_analyzer_addr: str = os.getenv("ORCH_ANALYZER_ADDR", "")
    orch_metta_addr: str = os.getenv("ORCH_METTA_ADDR", "")
    orch_resources_addr: str = os.getenv("ORCH_RESOURCES_ADDR", "")


settings = Settings()
