# Gmail-Trello Sync Automation 🚀

A clean, TypeScript-style Python automation to test Gmail-Trello synchronization.

## 📁 Project Structure

```
project/
├── models.py           # Data classes (Email, TrelloCard)
├── gmail_client.py     # Gmail API client
├── trello_client.py    # Trello API client
├── config.py           # Configuration constants
├── test_sync.py        # Main test suite
├── main.py             # Gmail authentication
└── requirements.txt    # Dependencies
```

## 🎯 Features

### Clean Architecture

-   **Type hints** throughout (like TypeScript interfaces!)
-   **Data classes** for Email and TrelloCard models
-   **Separation of concerns** - each file has one responsibility
-   **Client classes** for API interactions
-   **Pytest fixtures** for dependency injection

### Tests

1. **Connection Tests**

    - `test_trello_connection()` - Verify Trello API access
    - `test_gmail_connection()` - Verify Gmail API access

2. **Requirement 1: Urgent Emails Sync**

    - `test_requirement_1_urgent_emails_sync()`
    - Validates that emails with "Urgent" in body have Trello cards with "Urgent" label

3. **Requirement 2: Email Merging**
    - `test_requirement_2_email_merging()`
    - Validates that duplicate subject emails are merged into one Trello card

## 🚀 Usage

### Run All Tests

```bash
python -m pytest test_sync.py -v -s
```

### Run Specific Test

```bash
python -m pytest test_sync.py::test_requirement_1_urgent_emails_sync -v -s
```

### Run Only Connection Tests

```bash
python -m pytest test_sync.py::test_trello_connection -v -s
python -m pytest test_sync.py::test_gmail_connection -v -s
```

## 📚 Code Examples

### Creating Gmail Client

```python
from main import gmail_login
from gmail_client import GmailClient

creds = gmail_login()
gmail = GmailClient(creds)

# Get urgent emails
urgent_emails = gmail.get_urgent_emails()

# Get emails grouped by subject
grouped = gmail.get_emails_grouped_by_subject()
```

### Creating Trello Client

```python
from trello_client import TrelloClient
from config import TRELLO_API_KEY, TRELLO_API_TOKEN

trello = TrelloClient(TRELLO_API_KEY, TRELLO_API_TOKEN)

# Get all boards
boards = trello.get_boards()

# Get cards from a board
cards = trello.get_cards("My Board")

# Find specific card
card = trello.find_card_by_name("My Board", "Card Title")
```

### Working with Models

```python
from models import Email, TrelloCard

# Email model
email = Email(subject="Test", body="Urgent message")
print(email.is_urgent)  # True

# TrelloCard model
card = TrelloCard(
    id="123",
    name="Task",
    description="Description",
    labels=["Urgent", "Important"]
)
print(card.has_label("Urgent"))  # True
```

## 🎨 What Makes This Clean?

### ✅ Type Hints (TypeScript-like)

```python
def get_recent_emails(self, max_results: int = 50) -> List[Email]:
    """Get recent emails from inbox"""
    pass
```

### ✅ Data Classes (like TypeScript interfaces)

```python
@dataclass
class Email:
    subject: str
    body: str

    @property
    def is_urgent(self) -> bool:
        return "urgent" in self.body.lower()
```

### ✅ Dependency Injection (pytest fixtures)

```python
@pytest.fixture
def gmail_client() -> GmailClient:
    creds = gmail_login()
    return GmailClient(creds)

def test_something(gmail_client: GmailClient):
    emails = gmail_client.get_urgent_emails()
    # ... test logic
```

### ✅ Clean Test Structure (Given-When-Then)

```python
def test_requirement_1_urgent_emails_sync(gmail_client, trello_client):
    # Given: Get urgent emails
    urgent_emails = gmail_client.get_urgent_emails()

    # And: Get Trello cards
    cards = trello_client.get_cards("Board Name")

    # When & Then: Verify sync
    for email in urgent_emails:
        card = find_card_by_subject(cards, email.subject)
        assert card.has_label("Urgent")
```

## 📦 Dependencies

```
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
pytest
requests
```

## 🔧 Configuration

Edit `config.py` to change:

-   Trello credentials
-   Default board name
-   Max emails to check

## 🎓 Comparison: Before vs After

### Before (350 lines, all in one file)

```python
def test_trello_connection():
    url = "https://api.trello.com/1/members/me/boards"
    params = {"key": "...", "token": "..."}
    response = requests.get(url, params=params, verify=False)
    # ... 20 more lines
```

### After (Clean, focused, reusable)

```python
def test_trello_connection(trello_client: TrelloClient):
    boards = trello_client.get_boards()
    assert len(boards) > 0
```

**Much cleaner!** Like TypeScript! 🎉
