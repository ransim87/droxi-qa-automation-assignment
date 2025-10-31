from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Email:
    """Represents an email message"""
    subject: str
    body: str
    message_id: Optional[str] = None
    
    @property
    def is_urgent(self) -> bool:
        """Check if email contains 'Urgent' in the body"""
        return "urgent" in self.body.lower()
    
    def __repr__(self) -> str:
        return f"Email(subject='{self.subject[:50]}...', is_urgent={self.is_urgent})"


@dataclass
class TrelloCard:
    """Represents a Trello card"""
    id: str
    name: str
    description: str
    labels: List[str]
    
    def has_label(self, label_name: str) -> bool:
        """Check if card has a specific label"""
        return any(label.lower() == label_name.lower() for label in self.labels)
    
    def __repr__(self) -> str:
        return f"TrelloCard(name='{self.name}', labels={self.labels})"

