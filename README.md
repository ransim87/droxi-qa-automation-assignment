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
    ```bash
    cp src/config.py.template src/config.py
    ```
    - Edit `src/config.py` with your credentials:
        - API Key: https://trello.com/app-key
        - API Token: https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&name=Trello%20API&key=YOUR_API_KEY

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

## Notes

-   `credentials.json`, `token.json`, and `src/config.py` are excluded from git
-   Use `src/config.py.template` as reference only
-   Never commit real credentials
