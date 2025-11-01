import re

STATUSES = ["To Do", "In Progress", "Done"]
QUOTES = '"\'"\'\'\'\u201C\u201D\u2018\u2019'
INVALID_DESCRIPTION_TEXT = ["Edit", "Add a more detailed description…", ""]


def _normalize_whitespace(text):
    text = re.sub(r'[\n\r\t]+', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()


def _remove_quotes(text):
    for quote in QUOTES:
        text = text.replace(quote, '')
    return text.strip()


def _try_click(page, selector, timeout=2000):
    try:
        elem = page.locator(selector)
        if elem.is_visible(timeout=timeout):
            elem.click()
            page.wait_for_timeout(500)
    except:
        pass


def _get_text_from_selectors(page, selectors, is_textarea=False):
    for selector in selectors:
        try:
            elem = page.locator(selector).first
            if elem.is_visible(timeout=1000):
                text = elem.input_value() if is_textarea else elem.inner_text()
                text = text.strip()
                if text:
                    return text
        except:
            continue
    return ""


def _find_status_in_text(text):
    text = text.strip()
    if text in STATUSES:
        return text
    for status in STATUSES:
        if status in text and len(text) < 50:
            return status
    return None


class TrelloLoginPage:
    # Locators
    BUTTON_ALREADY_HAVE_ACCOUNT = "button:has-text('Already have an account? Log in')"
    INPUT_EMAIL = "input[type='email']"
    BUTTON_CONTINUE = "button:has-text('Continue')"
    INPUT_PASSWORD = "input[type='password']"
    BUTTON_LOGIN = "button:has-text('Log in')"
    
    def __init__(self, page):
        self.page = page
    
    def login(self, email, password):
        self.page.wait_for_timeout(2000)
        
        # Check if already logged in and on the board
        if "/b/2GzdgPlw/droxi" in self.page.url:
            return
        
        # Handle "Sign up" popup
        if "Sign up to see this board" in self.page.content():
            self.page.click(self.BUTTON_ALREADY_HAVE_ACCOUNT)
            self.page.wait_for_timeout(2000)
        
        # Fill email and continue
        self.page.fill(self.INPUT_EMAIL, email)
        self.page.click(self.BUTTON_CONTINUE)
        self.page.wait_for_selector(self.INPUT_PASSWORD, timeout=10000)
        
        # Fill password and login
        self.page.fill(self.INPUT_PASSWORD, password)
        self.page.click(self.BUTTON_LOGIN)
        
        # Wait for navigation to board
        self.page.wait_for_url("**/droxi", timeout=30000)
        self.page.wait_for_timeout(2000)


class TrelloBoardPage:
    # Locators
    BUTTON_ACCEPT_ALL = 'button:has-text("Accept all")'
    BUTTON_CLOSE = 'button:has-text("Close")'
    BUTTON_CLEAR_ALL = 'button:has-text("Clear all")'
    CARD_NAME = 'a[data-testid="card-name"]'
    
    # URL
    BOARD_URL = "https://trello.com/b/2GzdgPlw/droxi"
    
    def __init__(self, page):
        self.page = page
    
    def navigate(self):
        self.page.goto(self.BOARD_URL)
        self.page.wait_for_timeout(2000)
    
    def close_popups(self):
        _try_click(self.page, self.BUTTON_ACCEPT_ALL)
        _try_click(self.page, self.BUTTON_CLOSE)
        _try_click(self.page, self.BUTTON_CLEAR_ALL)
    
    def wait_for_board_ready(self):
        self.page.wait_for_load_state('networkidle', timeout=15000)
        
        # Try multiple ways to detect board is ready
        board_ready = False
        
        # Method 1: Check for status columns
        status_selector = ', '.join([f'h2:has-text("{s}")' for s in STATUSES])
        try:
            self.page.wait_for_selector(status_selector, timeout=5000)
            board_ready = True
        except:
            pass
        
        # Method 2: Check for card links
        if not board_ready:
            try:
                self.page.wait_for_selector(self.CARD_NAME, timeout=5000)
                board_ready = True
            except:
                pass
        
        # Method 3: Check URL
        if not board_ready:
            if "/b/2GzdgPlw/droxi" in self.page.url:
                board_ready = True
        
        # If still not ready, wait a bit more and check again
        if not board_ready:
            self.page.wait_for_timeout(3000)
            try:
                self.page.wait_for_selector('h2, a[data-testid="card-name"]', timeout=3000)
            except:
                pass  # Continue anyway - board might be ready
        
        self.page.wait_for_timeout(1000)
    
    def apply_urgent_filter(self):
        self.page.goto(f"{self.BOARD_URL}?filter=label:Urgent")
        self.page.wait_for_load_state('networkidle', timeout=10000)
        self.page.wait_for_timeout(1500)
    
    def _get_all_card_links(self):
        links = self.page.locator(self.CARD_NAME).all()
        return [link for link in links if link.is_visible()]
    
    def get_visible_cards(self):
        return self._get_all_card_links()
    
    def find_card_by_title(self, title):
        title_lower = title.lower()
        for link in self._get_all_card_links():
            if title_lower in link.inner_text().strip().lower():
                return link
        return None
    
    def get_card_column_status(self, card_link):
        if not card_link:
            return "Unknown"
        
        header_text = card_link.evaluate("""el => {
            let current = el;
            for (let i = 0; i < 15 && current; i++) {
                let container = current.closest('[data-list-id]') || current.closest('div[class*="list"]');
                if (container) {
                    let header = container.querySelector('h2');
                    if (header) return header.textContent.trim();
                }
                current = current.parentElement;
            }
            return null;
        }""")
        
        if header_text and header_text in STATUSES:
            return header_text
        
        try:
            card_box = card_link.bounding_box()
            if not card_box:
                return "Unknown"
            
            status_selector = ', '.join([f'h2:has-text("{s}")' for s in STATUSES])
            headers = self.page.locator(status_selector).all()
            
            for header in headers:
                if not header.is_visible(timeout=500):
                    continue
                header_box = header.bounding_box()
                if not header_box:
                    continue
                if (abs(card_box['x'] - header_box['x']) < 200 and
                    card_box['y'] >= header_box['y'] - 50 and
                    card_box['y'] <= header_box['y'] + 500):
                    status = header.inner_text().strip()
                    if status in STATUSES:
                        return status
        except:
            pass
        
        return "Unknown"
    
    def clear_filters(self):
        _try_click(self.page, self.BUTTON_CLEAR_ALL)


class TrelloCardDialog:
    # Locators
    DIALOG = 'div[role="dialog"]'
    TITLE_TEXTAREA = 'textarea[data-testid="card-back-title-input"]'
    TITLE_INPUT = '[data-testid="card-back-title-input"]'
    TITLE_H2 = '[role="dialog"] h2'
    LABELS_CONTAINER = '[data-testid="card-back-labels-container"]'
    LABEL_COLOR = '[aria-label*="Color:"]'
    DESC_CONTAINER = '[data-testid="card-back-description-container"]'
    DESC_PARAGRAPH = 'p'
    DESC_TEXTAREA = 'textarea, [contenteditable="true"]'
    DIALOG_PARAGRAPHS = '[role="dialog"] p'
    LIST_NAME = '[data-testid="card-back-list-name"]'
    DIALOG_LINKS_BUTTONS = '[role="dialog"] a, [role="dialog"] button'
    
    # Title selectors (ordered by priority)
    TITLE_SELECTORS = [
        'textarea[data-testid="card-back-title-input"]',
        '[data-testid="card-back-title-input"]',
        '[role="dialog"] h2',
    ]
    
    def __init__(self, page):
        self.page = page
    
    def open_card(self, card_link):
        card_link.click()
        self.page.wait_for_timeout(1500)
        self.page.wait_for_selector(self.DIALOG, timeout=5000)
        self.page.wait_for_timeout(800)
    
    def get_title(self):
        return _get_text_from_selectors(self.page, self.TITLE_SELECTORS, is_textarea=True)
    
    def get_labels(self):
        labels = []
        container = self.page.locator(self.LABELS_CONTAINER).first
        
        if not container.is_visible(timeout=1000):
            return labels
        
        for element in container.locator(self.LABEL_COLOR).all():
            aria_label = element.get_attribute('aria-label')
            if not aria_label or 'title:' not in aria_label:
                continue
            
            label_text = aria_label.split('title:')[1].strip()
            label_name = _remove_quotes(label_text)
            
            if label_name and label_name not in labels:
                labels.append(label_name)
        
        return labels
    
    def get_description(self):
        desc_section = self.page.locator(self.DESC_CONTAINER).first
        
        try:
            if desc_section.count() > 0:
                desc_text = desc_section.locator(self.DESC_PARAGRAPH).first
                if desc_text.count() > 0:
                    try:
                        text = desc_text.inner_text(timeout=500).strip()
                        if text and text not in INVALID_DESCRIPTION_TEXT:
                            return _normalize_whitespace(text)
                    except:
                        pass
                
                desc_textarea = desc_section.locator(self.DESC_TEXTAREA).first
                if desc_textarea.count() > 0:
                    try:
                        text = desc_textarea.inner_text(timeout=500).strip()
                        if text and text not in INVALID_DESCRIPTION_TEXT:
                            return _normalize_whitespace(text)
                    except:
                        pass
        except:
            pass
        
        paragraphs = self.page.locator(self.DIALOG_PARAGRAPHS).all()
        for para in paragraphs:
            try:
                text = para.inner_text(timeout=500).strip()
                if (text and 5 < len(text) < 500 and
                    text not in INVALID_DESCRIPTION_TEXT and
                    not text.lower().startswith("add")):
                    return _normalize_whitespace(text)
            except:
                continue
        
        return ""
    
    def get_status(self):
        list_name = self.page.locator(self.LIST_NAME).first
        if list_name.is_visible(timeout=2000):
            status = _find_status_in_text(list_name.inner_text())
            if status:
                return status
        
        for elem in self.page.locator(self.DIALOG_LINKS_BUTTONS).all():
            if not elem.is_visible(timeout=500):
                continue
            status = _find_status_in_text(elem.inner_text())
            if status:
                return status
        
        dialog = self.page.locator(self.DIALOG).first
        if dialog.is_visible(timeout=1000):
            for line in dialog.inner_text().split('\n')[:10]:
                status = _find_status_in_text(line)
                if status:
                    return status
        
        return "Unknown"
    
    def close(self):
        self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(500)
