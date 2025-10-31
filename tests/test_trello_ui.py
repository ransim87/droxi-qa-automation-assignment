import pytest
from playwright.sync_api import sync_playwright
from src.pages.trello_page import TrelloLoginPage, TrelloBoardPage, TrelloCardDialog


@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        yield browser


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page


def test_extract_urgent_cards(page):
    """Extract all urgent cards with their details from Trello board"""
    
    login_page = TrelloLoginPage(page)
    board_page = TrelloBoardPage(page)
    card_dialog = TrelloCardDialog(page)
    
    board_page.navigate()
    login_page.login("droxiautomation@gmail.com", "Droxination013!")
    board_page.close_popups()
    board_page.wait_for_board_ready()
    
    print("\nFiltering for urgent cards...")
    board_page.apply_urgent_filter()
    
    card_links = board_page.get_visible_cards()
    print(f"Found {len(card_links)} urgent cards\n")
    
    urgent_cards = []
    
    for card_link in card_links:
        try:
            title = card_link.inner_text().strip()
            if not title:
                continue
            
            card_dialog.open_card(card_link)
            
            card_data = {
                'title': title,
                'labels': card_dialog.get_labels(),
                'description': card_dialog.get_description(),
                'status': card_dialog.get_status()
            }
            
            urgent_cards.append(card_data)
            
            print(f"Card: {card_data['title']}")
            print(f"  Labels: {', '.join(card_data['labels'])}")
            print(f"  Description: {card_data['description']}")
            print(f"  Status: {card_data['status']}\n")
            
            card_dialog.close()
            
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
        has_urgent = any('urgent' in label.lower() for label in card['labels'])
    
    return urgent_cards

