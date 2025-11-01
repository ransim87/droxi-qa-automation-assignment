import os
import pytest
from playwright.sync_api import sync_playwright
from src.pages.trello_page import TrelloLoginPage, TrelloBoardPage, TrelloCardDialog

EMAIL = os.getenv("TRELLO_EMAIL", "droxiautomation@gmail.com")
PASSWORD = os.getenv("TRELLO_PASSWORD", "Droxination013!")


@pytest.fixture(scope="function")
def browser():
    headless = os.getenv("CI", "false").lower() == "true"
    slow_mo = 0 if headless else 500
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        yield browser


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page


@pytest.fixture
def trello_pages(page):
    """Setup Trello pages and login."""
    login_page = TrelloLoginPage(page)
    board_page = TrelloBoardPage(page)
    card_dialog = TrelloCardDialog(page)
    
    board_page.navigate()
    login_page.login(EMAIL, PASSWORD)
    board_page.close_popups()
    board_page.wait_for_board_ready()
    
    return login_page, board_page, card_dialog


def extract_card_data(card_dialog, card_link):
    """Extract all data from a card."""
    title = card_link.inner_text().strip()
    if not title:
        return None
    
    card_dialog.open_card(card_link)
    data = {
        'title': title,
        'labels': card_dialog.get_labels(),
        'description': card_dialog.get_description(),
        'status': card_dialog.get_status()
    }
    card_dialog.close()
    return data


def test_extract_urgent_cards(page, trello_pages):
    """Extract all urgent cards with their details from Trello board"""
    _, board_page, card_dialog = trello_pages
    
    print("\nFiltering for urgent cards...")
    board_page.apply_urgent_filter()
    
    card_links = board_page.get_visible_cards()
    print(f"Found {len(card_links)} urgent cards\n")
    
    urgent_cards = []
    for card_link in card_links:
        try:
            data = extract_card_data(card_dialog, card_link)
            if data:
                urgent_cards.append(data)
                print(f"Card: {data['title']}")
                print(f"  Labels: {', '.join(data['labels'])}")
                print(f"  Description: {data['description']}")
                print(f"  Status: {data['status']}\n")
        except Exception as e:
            print(f"Error processing card: {e}")
            try:
                card_dialog.close()
            except:
                pass
    
    board_page.clear_filters()
    print(f"\nTotal urgent cards: {len(urgent_cards)}")
    
    assert len(urgent_cards) >= 1, "Should find at least one urgent card"
    for card in urgent_cards:
        assert card['title'], "Card must have a title"


def test_specific_card_validation(page, trello_pages):
    """Scenario 2: Validate specific card 'summarize the meeting' details"""
    _, board_page, card_dialog = trello_pages
    
    card_title = "summarize the meeting"
    card_link = board_page.find_card_by_title(card_title)
    assert card_link is not None, f"Card '{card_title}' not found on the board"
    
    card_link_title = card_link.inner_text().strip()
    board_status = board_page.get_card_column_status(card_link)
    
    card_dialog.open_card(card_link)
    
    actual_title = card_dialog.get_title() or card_link_title
    assert actual_title.lower() == card_title.lower(), \
        f"Card title mismatch. Expected: '{card_title}', Actual: '{actual_title}'"
    
    expected_description = "For all of us Please do so"
    actual_description = card_dialog.get_description()
    assert actual_description == expected_description, \
        f"Description mismatch. Expected: '{expected_description}', Actual: '{actual_description}'"
    
    labels = card_dialog.get_labels()
    assert "New" in labels, f"'New' label not found. Found labels: {labels}"
    
    dialog_status = card_dialog.get_status()
    status = dialog_status if dialog_status != "Unknown" else board_status
    assert status == "To Do", \
        f"Card status mismatch. Expected: 'To Do', Actual: '{status}'"
    
    card_dialog.close()
    board_page.wait_for_board_ready()
    
    print(f"\n✓ Card validation passed:")
    print(f"  Title: {actual_title}")
    print(f"  Description: {actual_description}")
    print(f"  Labels: {', '.join(labels)}")
    print(f"  Status: {status}")
