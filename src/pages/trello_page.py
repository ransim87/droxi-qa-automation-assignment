class TrelloLoginPage:
    def __init__(self, page):
        self.page = page
    
    def login(self, email, password):
        if "Sign up to see this board" in self.page.content():
            self.page.click("button:has-text('Already have an account? Log in')")
            self.page.wait_for_timeout(1500)
        
        if "login" in self.page.url:
            self.page.fill("input[type='email']", email)
            self.page.click("button:has-text('Continue')")
            self.page.wait_for_selector("input[type='password']")
            self.page.fill("input[type='password']", password)
            self.page.click("button:has-text('Log in')")
            self.page.wait_for_url("**/b/2GzdgPlw/droxi**", timeout=10000)
            self.page.wait_for_timeout(1500)


class TrelloBoardPage:
    def __init__(self, page):
        self.page = page
        self.board_url = "https://trello.com/b/2GzdgPlw/droxi"
    
    def navigate(self):
        self.page.goto(self.board_url)
        self.page.wait_for_timeout(2000)
    
    def close_popups(self):
        self._accept_cookies()
        self._close_jira_promo()
        self._clear_existing_filters()
    
    def _accept_cookies(self):
        try:
            accept_btn = self.page.locator('button:has-text("Accept all")')
            if accept_btn.is_visible(timeout=2000):
                accept_btn.click()
                self.page.wait_for_timeout(1000)
        except:
            pass
    
    def _close_jira_promo(self):
        try:
            close_btn = self.page.locator('button:has-text("Close")').last
            if close_btn.is_visible(timeout=2000):
                close_btn.click()
                self.page.wait_for_timeout(500)
        except:
            pass
    
    def _clear_existing_filters(self):
        try:
            clear_btn = self.page.locator('button:has-text("Clear all")')
            if clear_btn.is_visible(timeout=2000):
                clear_btn.click()
                self.page.wait_for_timeout(1000)
        except:
            pass
    
    def wait_for_board_ready(self):
        self.page.wait_for_load_state('networkidle', timeout=10000)
        self.page.wait_for_selector('h2:has-text("To Do"), h2:has-text("In Progress"), h2:has-text("Done")', timeout=10000)
        self.page.wait_for_timeout(1000)
    
    def apply_urgent_filter(self):
        self.page.goto(f"{self.board_url}?filter=label:Urgent")
        self.page.wait_for_load_state('networkidle', timeout=10000)
        self.page.wait_for_timeout(1500)
    
    def get_visible_cards(self):
        all_links = self.page.locator('a[data-testid="card-name"]').all()
        return [link for link in all_links if link.is_visible()]
    
    def clear_filters(self):
        try:
            clear_btn = self.page.locator('button:has-text("Clear all")')
            if clear_btn.is_visible(timeout=2000):
                clear_btn.click()
                self.page.wait_for_timeout(1000)
        except:
            pass


class TrelloCardDialog:
    def __init__(self, page):
        self.page = page
    
    def open_card(self, card_link):
        card_link.click()
        self.page.wait_for_timeout(1500)
        self.page.wait_for_selector('div[role="dialog"]', timeout=5000)
        self.page.wait_for_timeout(800)
    
    def get_labels(self):
        labels = []
        container = self.page.locator('[data-testid="card-back-labels-container"]').first
        
        if container.is_visible(timeout=1000):
            elements = container.locator('[aria-label*="Color:"]').all()
            for element in elements:
                aria_label = element.get_attribute('aria-label')
                if aria_label and 'title:' in aria_label:
                    label_text = aria_label.split('title:')[1].strip()
                    label_name = label_text.replace('"', '').replace("'", '').strip()
                    if label_name and label_name not in labels:
                        labels.append(label_name)
        
        return labels
    
    def get_description(self):
        try:
            paragraphs = self.page.locator('[role="dialog"] p').all()
            for para in paragraphs:
                if para.is_visible(timeout=500):
                    text = para.inner_text().strip()
                    if text and text not in ["Edit", "Add a more detailed description…", ""] and len(text) < 200:
                        return text
        except:
            pass
        return "No description"
    
    def get_status(self):
        try:
            first_button = self.page.locator('[role="dialog"] button').first
            if first_button.is_visible(timeout=1000):
                status = first_button.inner_text().strip()
                if status in ["To Do", "In Progress", "Done"]:
                    return status
        except:
            pass
        return "Unknown"
    
    def close(self):
        self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(500)

