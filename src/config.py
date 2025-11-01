import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Trello API credentials (required - set via environment variables)
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")

if not TRELLO_API_KEY:
    raise ValueError(
        "TRELLO_API_KEY environment variable is required. "
        "Set it in your environment or create a .env file."
    )

if not TRELLO_API_TOKEN:
    raise ValueError(
        "TRELLO_API_TOKEN environment variable is required. "
        "Set it in your environment or create a .env file."
    )

# Test configuration
DEFAULT_BOARD_NAME = os.getenv("DEFAULT_BOARD_NAME", "Droxi")
MAX_EMAILS_TO_CHECK = int(os.getenv("MAX_EMAILS_TO_CHECK", "50"))

