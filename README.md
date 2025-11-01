# Gmail-Trello Sync Automation

Python Playwright automation project for testing Gmail-Trello synchronization.

## Project Structure

```
src/
├── models.py              # Data models (Email, TrelloCard)
├── config.py              # Configuration (create from template)
├── clients/
│   ├── gmail_client.py    # Gmail API client
│   └── trello_client.py   # Trello API client
└── pages/
    └── trello_page.py     # Playwright page objects

tests/
├── test_sync.py           # API tests
└── test_trello_ui.py      # UI tests (Playwright)
```

## Setup

### Prerequisites

-   Python 3.8+
-   Gmail API credentials
-   Trello API credentials

### Installation

1. Clone repository

    ```bash
    git clone <repository-url>
    cd python-playwright
    ```

2. Create virtual environment

    ```bash
    python -m venv venv
    venv\Scripts\activate      # Windows
    source venv/bin/activate   # Linux/Mac
    ```

3. Install dependencies

    ```bash
    pip install -r requirements.txt
    playwright install
    ```

4. Configure Gmail API

    - Download OAuth credentials from [Google Cloud Console](https://console.cloud.google.com/)
    - Save as `credentials.json` in project root
    - First run will create `token.json` automatically

5. Configure Trello API
   Create a `.env` file in the project root:
    ```bash
    TRELLO_API_KEY=your-api-key-here
    TRELLO_API_TOKEN=your-api-token-here
    ```
    - Get your API Key: https://trello.com/app-key
    - Get your API Token: https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&name=Trello%20API&key=YOUR_API_KEY
    - The `.env` file is automatically ignored by git

## Dependencies

-   google-api-python-client
-   google-auth-httplib2
-   google-auth-oauthlib
-   pytest
-   requests
-   pytest-playwright
-   playwright

Install: `pip install -r requirements.txt`

## Configuration

### Gmail

-   `credentials.json` - OAuth credentials (not in git)
-   `token.json` - Auto-generated access token (not in git)

### Trello

Edit `src/config.py`:

```python
TRELLO_API_KEY = "your-key"
TRELLO_API_TOKEN = "your-token"
DEFAULT_BOARD_NAME = "Droxi"
MAX_EMAILS_TO_CHECK = 50
```

## Running Tests

Run all tests:

```bash
python -m pytest tests/ -v -s
```

Run specific suite:

```bash
python -m pytest tests/test_sync.py -v -s          # API tests
python -m pytest tests/test_trello_ui.py -v -s      # UI tests
python -m pytest tests/test_trello_ui.py --headed   # UI with browser
```

Run specific test:

```bash
python -m pytest tests/test_sync.py::test_trello_connection -v
```

## Tests

-   `test_trello_connection()` - Trello API access
-   `test_gmail_connection()` - Gmail API access
-   `test_urgent_emails_sync()` - Urgent emails have Urgent label in Trello
-   `test_email_merging()` - Duplicate subject emails merge into one card

## Troubleshooting

**Gmail authentication fails:**

-   Verify `credentials.json` exists in project root
-   Delete `token.json` and re-authenticate
-   Ensure Gmail API is enabled in Google Cloud Console

**Trello API errors:**

-   Check API key and token in `src/config.py`
-   Board name must match exactly (case-sensitive)
-   Verify API rate limits

**Playwright issues:**

-   Run `playwright install`
-   Use `--headed` flag to debug browser issues

## GitHub Actions

Automated tests run on push and pull requests via GitHub Actions.

### Required Secrets

Configure these secrets in your GitHub repository settings (Settings → Secrets and variables → Actions):

-   `TRELLO_API_KEY` - Your Trello API key
-   `TRELLO_API_TOKEN` - Your Trello API token
-   `TRELLO_EMAIL` - Trello account email for UI tests
-   `TRELLO_PASSWORD` - Trello account password for UI tests

The workflow runs tests on Python 3.10, 3.11, and 3.12.

## Notes

-   `credentials.json`, `token.json`, and `.env` are excluded from git
-   Never commit real credentials
-   Tests run in headless mode in CI automatically
-   Create a `.env` file for local development (see setup instructions above)
