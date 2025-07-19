"""
Gmail API service operations
"""

import structlog
from typing import List, Dict, Optional

from googleapiclient.errors import HttpError

from .config import DEFAULT_MAX_RESULTS

logger = structlog.get_logger()


class GmailService:
    """Handles Gmail API operations"""
    
    def __init__(self, service):
        self.service = service
    
    def get_label_id(self, label_name: str) -> Optional[str]:
        """Get label ID from label name"""
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            for label in labels:
                if label['name'].lower() == label_name.lower():
                    return label['id']
            
            return None
        except HttpError as error:
            logger.error("label_id_error", error=str(error), label_name=label_name)
            return None
    
    def create_label(self, label_name: str) -> Optional[str]:
        """Create a new label"""
        try:
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            label = self.service.users().labels().create(
                userId='me',
                body=label_object
            ).execute()
            logger.info("label_created", label_name=label_name)
            return label['id']
        except HttpError as error:
            logger.error("label_create_error", error=str(error), label_name=label_name)
            return None
    
    def get_emails_with_label(self, label_name: str, max_results: int = DEFAULT_MAX_RESULTS) -> List[Dict]:
        """Get emails with specific label"""
        label_id = self.get_label_id(label_name)
        if not label_id:
            logger.warning("label_not_found", label_name=label_name)
            return []
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=[label_id],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            logger.info("emails_found", count=len(messages), label_name=label_name)
            return messages
            
        except HttpError as error:
            logger.error("email_retrieval_error", error=str(error))
            return []
    
    def get_email_details(self, msg_id: str) -> Optional[Dict]:
        """Get full email details including headers"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            return message
        except HttpError as error:
            logger.error("email_details_error", error=str(error), msg_id=msg_id)
            return None
    
    def add_label_to_message(self, msg_id: str, label_name: str) -> bool:
        """Add a label to an email"""
        label_id = self.get_label_id(label_name)
        if not label_id:
            label_id = self.create_label(label_name)
            if not label_id:
                return False
        
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            return True
        except HttpError as error:
            logger.error("add_label_error", error=str(error), msg_id=msg_id, label_name=label_name)
            return False
    
    def remove_label_from_message(self, msg_id: str, label_name: str) -> bool:
        """Remove a label from an email"""
        label_id = self.get_label_id(label_name)
        if not label_id:
            return False
        
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': [label_id]}
            ).execute()
            return True
        except HttpError as error:
            logger.error("remove_label_error", error=str(error), msg_id=msg_id, label_name=label_name)
            return False
    
    def send_message(self, message_body: Dict) -> Optional[Dict]:
        """Send an email message"""
        try:
            result = self.service.users().messages().send(
                userId='me',
                body=message_body
            ).execute()
            return result
        except HttpError as error:
            logger.error("send_message_error", error=str(error))
            return None