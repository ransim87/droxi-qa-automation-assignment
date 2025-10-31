"""
Gmail API client for reading emails
"""
import base64
from typing import List, Dict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from src.models import Email


class GmailClient:
    """Client for interacting with Gmail API"""
    
    def __init__(self, credentials: Credentials):
        """Initialize Gmail client with credentials"""
        self.service = build("gmail", "v1", credentials=credentials)
    
    def get_recent_emails(self, max_results: int = 50) -> List[Email]:
        """
        Get recent emails from inbox
        
        Args:
            max_results: Maximum number of emails to retrieve
            
        Returns:
            List of Email objects
        """
        results = self.service.users().messages().list(
            userId="me", 
            maxResults=max_results
        ).execute()
        
        message_ids = results.get("messages", [])
        emails = []
        
        for msg_data in message_ids:
            message = self.service.users().messages().get(
                userId="me", 
                id=msg_data["id"], 
                format="full"
            ).execute()
            
            subject = self._extract_subject(message)
            body = self._extract_body(message)
            
            emails.append(Email(
                subject=subject,
                body=body,
                message_id=msg_data["id"]
            ))
        
        return emails
    
    def get_urgent_emails(self, max_results: int = 50) -> List[Email]:
        """Get only emails that are marked as urgent"""
        all_emails = self.get_recent_emails(max_results)
        return [email for email in all_emails if email.is_urgent]
    
    def get_emails_grouped_by_subject(self, max_results: int = 50) -> Dict[str, List[Email]]:
        """
        Get emails grouped by their subject
        
        Returns:
            Dictionary with subjects as keys and list of emails as values
        """
        all_emails = self.get_recent_emails(max_results)
        grouped: Dict[str, List[Email]] = {}
        
        for email in all_emails:
            if email.subject not in grouped:
                grouped[email.subject] = []
            grouped[email.subject].append(email)
        
        return grouped
    
    def _extract_subject(self, message: Dict) -> str:
        """Extract subject from Gmail message"""
        headers = message.get("payload", {}).get("headers", [])
        for header in headers:
            if header["name"].lower() == "subject":
                return header["value"]
        return ""
    
    def _extract_body(self, message: Dict) -> str:
        """Extract body text from Gmail message"""
        payload = message.get("payload", {})
        
        # Try simple body
        if "body" in payload and "data" in payload["body"]:
            return self._decode_body(payload["body"]["data"])
        
        # Try multipart body
        if "parts" in payload:
            body = ""
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    if "data" in part.get("body", {}):
                        body += self._decode_body(part["body"]["data"])
            return body
        
        return ""
    
    def _decode_body(self, data: str) -> str:
        """Decode base64url encoded body"""
        try:
            decoded_bytes = base64.urlsafe_b64decode(data)
            return decoded_bytes.decode("utf-8")
        except Exception:
            return ""

