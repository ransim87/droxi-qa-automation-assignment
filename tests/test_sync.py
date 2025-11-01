import os
import pytest
from main import gmail_login
from src.clients.gmail_client import GmailClient
from src.clients.trello_client import TrelloClient
from src.config import TRELLO_API_KEY, TRELLO_API_TOKEN, DEFAULT_BOARD_NAME

@pytest.fixture(scope="module")
def gmail_client():
    if not os.path.exists("credentials.json"):
        pytest.skip("credentials.json not found - Gmail tests require Gmail credentials")
    try:
        return GmailClient(gmail_login())
    except FileNotFoundError:
        pytest.skip("credentials.json not found - Gmail tests require Gmail credentials")


@pytest.fixture(scope="module")
def trello_client():
    return TrelloClient(TRELLO_API_KEY, TRELLO_API_TOKEN)


@pytest.fixture(scope="module")
def urgent_emails(gmail_client):
    return gmail_client.get_urgent_emails()


@pytest.fixture(scope="module")
def trello_cards(trello_client):
    return trello_client.get_cards(DEFAULT_BOARD_NAME)


def test_trello_connection(trello_client):
    boards = trello_client.get_boards()
    assert len(boards) > 0, "No Trello boards found"


def test_gmail_connection(gmail_client):
    emails = gmail_client.get_recent_emails(max_results=5)
    assert len(emails) >= 0


def test_urgent_emails_sync(urgent_emails, trello_cards):
    missing_cards = []
    missing_labels = []
    
    for email in urgent_emails:
        card = next((c for c in trello_cards if c.name == email.subject), None)
        
        if not card:
            missing_cards.append(email.subject)
        elif not card.has_label("Urgent"):
            missing_labels.append(email.subject)
    
    assert not missing_cards, f"Missing cards: {missing_cards}"
    assert not missing_labels, f"Missing Urgent label: {missing_labels}"


def test_email_merging(gmail_client, trello_client):
    emails_by_subject = gmail_client.get_emails_grouped_by_subject()
    cards = trello_client.get_cards(DEFAULT_BOARD_NAME)
    issues = []
    
    for subject, emails in emails_by_subject.items():
        if len(emails) <= 1:
            continue
            
        unique_bodies = set(e.body.strip() for e in emails if e.body.strip())
        if len(unique_bodies) <= 1:
            continue
        
        card_title = subject.replace("Task: ", "") if subject.startswith("Task: ") else subject
        card = next((c for c in cards if c.name == card_title), None)
        
        if not card:
            continue
        
        for email in emails:
            if email.body.strip() and email.body.strip() not in card.description:
                issues.append(f"Card '{card_title}' missing email body")
                break
    
    assert not issues, f"Issues found: {issues}"

