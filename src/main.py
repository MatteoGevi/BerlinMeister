import os
import json
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from scrapers.immoscout24 import ImmoscoutScraper
from notification import EmailNotifier

# Load environment variables
load_dotenv()

class ApartmentFinder:
    def __init__(self):
        self.email_notifier = EmailNotifier()
        self.scrapers = [
            ImmoscoutScraper()
        ]
        self.seen_listings = set()
        self.load_seen_listings()

    def load_seen_listings(self):
        try:
            with open('data/seen_listings.json', 'r') as f:
                self.seen_listings = set(json.load(f))
        except FileNotFoundError:
            self.seen_listings = set()

    def save_seen_listings(self):
        os.makedirs('data', exist_ok=True)
        with open('data/seen_listings.json', 'w') as f:
            json.dump(list(self.seen_listings), f)

    def check_new_listings(self):
        new_listings = []
        for scraper in self.scrapers:
            listings = scraper.get_listings()
            for listing in listings:
                if listing['id'] not in self.seen_listings:
                    new_listings.append(listing)
                    self.seen_listings.add(listing['id'])
        
        if new_listings:
            self.email_notifier.send_notification(new_listings)
            self.save_seen_listings()

    def run(self):
        print("Starting Berlin Apartment Finder...")
        schedule.every(30).minutes.do(self.check_new_listings)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    finder = ApartmentFinder()
    finder.run() 