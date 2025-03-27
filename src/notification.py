import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv

class EmailNotifier:
    def __init__(self):
        load_dotenv()
        self.email_address = os.getenv('EMAIL_ADDRESS')

    def format_listing(self, listing):
        return f"""
        🏠 New Apartment Found!
        
        Price: {listing['price']}€
        Size: {listing['size']} m²
        Rooms: {listing['rooms']}
        Location: {listing['location']}
        
        Description: {listing['description'][:200]}...
        
        Link: {listing['url']}
        
        Found on: {listing['source']}
        """

    def send_notification(self, listings):
        if not listings:
            return

        subject = f"🏠 New Berlin Apartments Found - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        body = "Here are the new apartments that match your criteria:\n\n"
        for listing in listings:
            body += self.format_listing(listing) + "\n" + "-"*50 + "\n"

        # Using the MCP Gmail action to send the email
        try:
            self.send_email_mcp(subject, body)
            print(f"Successfully sent notification about {len(listings)} new listings")
        except Exception as e:
            print(f"Failed to send email notification: {str(e)}")

    def send_email_mcp(self, subject, body):
        return {
            "subject": subject,
            "body": body,
            "to": self.email_address
        } 