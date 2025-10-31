# Gmail-Trello Sync Automation

QA Automation project for testing Gmail-Trello synchronization using Python and Playwright.

## 📁 Project Structure

```
python-playwright/
├── src/
│   ├── models.py           # Data classes (Email, TrelloCard)
│   ├── config.py           # Configuration constants (create from template)
│   ├── clients/
│   │   ├── gmail_client.py     # Gmail API client
│   │   └── trello_client.py    # Trello API client
│   └── pages/
│       └── trello_page.py      # Trello UI page objects (Playwright)
├── tests/
│   ├── test_sync.py        # Main API test suite
│   └── test_trello_ui.py   # UI tests using Playwright
├── main.py                 # Gmail authentication
├── requirements.txt        # Python dependencies
└── pytest.ini             # Pytest configuration
```

## 🚀 Setup

### Prerequisites

-   Python 3.8 or higher
-   Gmail account with API access
-   Trello account with API credentials

### Installation Steps

1. **Clone the repository**

    ```bash
    git clone <repository-url>
    cd python-playwright
    ```

2. **Create a virtual environment** (recommended)

    ```bash
    python -m venv venv

    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install Playwright browsers**

    ```bash
    playwright install
    ```

5. **Configure Gmail API credentials**

    - Download OAuth 2.0 credentials from [Google Cloud Console](https://console.cloud.google.com/)
    - Save the credentials file as `credentials.json` in the project root
    - On first run, the script will open a browser for authentication and create `token.json`

6. **Configure Trello API credentials**
    - Copy the template file:
        ```bash
        cp src/config.py.template src/config.py
        ```
    - Edit `src/config.py` and add your Trello credentials:
        - Get your API key from: https://trello.com/app-key
        - Generate an API token from: https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&name=Trello%20API&key=YOUR_API_KEY
        - Update `TRELLO_API_KEY` and `TRELLO_API_TOKEN` in `src/config.py`

## 📦 Dependencies

The following Python packages are required:

```
google-api-python-client      # Gmail API client
google-auth-httplib2         # Google authentication
google-auth-oauthlib         # OAuth 2.0 flow
pytest                       # Testing framework
requests                     # HTTP library for Trello API
pytest-playwright            # Playwright plugin for pytest
playwright                   # Browser automation
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## 🔧 Environment Variables and Configuration

### Gmail API Setup

1. **OAuth Credentials**: Place `credentials.json` in the project root directory

    - This file contains your OAuth 2.0 client ID and secret
    - Never commit this file to version control

2. **Access Token**: The `token.json` file will be created automatically after first authentication
    - This file stores your access and refresh tokens
    - Never commit this file to version control

### Trello API Setup

Edit `src/config.py` with your Trello credentials:

```python
TRELLO_API_KEY = "your-api-key-here"
TRELLO_API_TOKEN = "your-api-token-here"
DEFAULT_BOARD_NAME = "Droxi"  # Name of your Trello board
MAX_EMAILS_TO_CHECK = 50       # Maximum emails to process
```

## 🧪 Running Tests

### Run All Tests

```bash
python -m pytest tests/ -v -s
```

### Run API Tests Only

```bash
python -m pytest tests/test_sync.py -v -s
```

### Run UI Tests Only (Playwright)

```bash
python -m pytest tests/test_trello_ui.py -v -s
```

### Run Specific Test

```bash
python -m pytest tests/test_sync.py::test_trello_connection -v -s
python -m pytest tests/test_sync.py::test_gmail_connection -v -s
python -m pytest tests/test_sync.py::test_urgent_emails_sync -v -s
```

### Run with Playwright UI Mode (Interactive)

```bash
python -m pytest tests/test_trello_ui.py --headed -v
```

## 📋 Test Coverage

### Connection Tests

-   `test_trello_connection()` - Verifies Trello API access
-   `test_gmail_connection()` - Verifies Gmail API access

### Requirement 1: Urgent Emails Sync

-   `test_urgent_emails_sync()` - Validates that emails with "Urgent" in body have Trello cards with "Urgent" label

### Requirement 2: Email Merging

-   `test_email_merging()` - Validates that duplicate subject emails are merged into one Trello card

## 📚 Usage Examples

### Using Gmail Client

```python
from main import gmail_login
from src.clients.gmail_client import GmailClient

# Authenticate
creds = gmail_login()
gmail = GmailClient(creds)

# Get urgent emails
urgent_emails = gmail.get_urgent_emails()

# Get emails grouped by subject
grouped = gmail.get_emails_grouped_by_subject()
```

### Using Trello Client

```python
from src.clients.trello_client import TrelloClient
from src.config import TRELLO_API_KEY, TRELLO_API_TOKEN

trello = TrelloClient(TRELLO_API_KEY, TRELLO_API_TOKEN)

# Get all boards
boards = trello.get_boards()

# Get cards from a board
cards = trello.get_cards("Droxi")

# Find specific card
card = trello.find_card_by_name("Droxi", "Card Title")
```

### Using Playwright for UI Tests

```python
from playwright.sync_api import Page
from src.pages.trello_page import TrelloPage

def test_trello_ui(page: Page):
    trello_page = TrelloPage(page)
    trello_page.navigate_to_board("Droxi")
    cards = trello_page.get_card_titles()
    assert len(cards) > 0
```

## 🛠️ Troubleshooting

### Gmail Authentication Issues

-   Ensure `credentials.json` is in the project root
-   Delete `token.json` and re-authenticate if tokens expire
-   Check that Gmail API is enabled in Google Cloud Console

### Trello API Issues

-   Verify API key and token in `src/config.py`
-   Ensure the board name matches exactly (case-sensitive)
-   Check Trello API rate limits

### Playwright Issues

-   Run `playwright install` to ensure browsers are installed
-   Use `--headed` flag to see the browser during tests
-   Check browser installation with `playwright --version`

## 📝 Notes

-   The `token.json` and `credentials.json` files are excluded from version control (see `.gitignore`)
-   Always use `src/config.py.template` as a reference - never commit your actual `src/config.py` with real credentials
-   Playwright tests require browser installation via `playwright install`
