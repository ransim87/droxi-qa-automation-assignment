import requests
import urllib3
from typing import List, Optional
from src.models import TrelloCard

# Disable SSL warnings for corporate proxies
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TrelloClient:    
    BASE_URL = "https://api.trello.com/1"
    
    def __init__(self, api_key: str, api_token: str):
        self.api_key = api_key
        self.api_token = api_token
    
    def get_boards(self) -> List[dict]:
        url = f"{self.BASE_URL}/members/me/boards"
        response = requests.get(
            url, 
            params=self._auth_params(),
            verify=False
        )
        response.raise_for_status()
        return response.json()
    
    def get_board_id(self, board_name: str) -> Optional[str]:
        """Get board ID by name"""
        boards = self.get_boards()
        for board in boards:
            if board["name"] == board_name:
                return board["id"]
        return None
    
    def get_cards(self, board_name: str) -> List[TrelloCard]:
        """
        Get all cards from a board
        
        Args:
            board_name: Name of the Trello board
            
        Returns:
            List of TrelloCard objects
        """
        board_id = self.get_board_id(board_name)
        if not board_id:
            return []
        
        url = f"{self.BASE_URL}/boards/{board_id}/cards"
        response = requests.get(
            url,
            params=self._auth_params(),
            verify=False
        )
        response.raise_for_status()
        
        cards_data = response.json()
        cards = []
        
        for card_data in cards_data:
            label_names = [label["name"] for label in card_data.get("labels", [])]
            cards.append(TrelloCard(
                id=card_data["id"],
                name=card_data["name"],
                description=card_data.get("desc", ""),
                labels=label_names
            ))
        
        return cards
    
    def find_card_by_name(self, board_name: str, card_name: str) -> Optional[TrelloCard]:
        """Find a card by its name in a board"""
        cards = self.get_cards(board_name)
        for card in cards:
            if card.name == card_name:
                return card
        return None
    
    def _auth_params(self) -> dict:
        """Return authentication parameters"""
        return {
            "key": self.api_key,
            "token": self.api_token
        }

