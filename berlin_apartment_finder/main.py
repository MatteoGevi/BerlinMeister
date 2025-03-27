import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import schedule
import time

def check_immoscout24():
    """Check ImmobilienScout24 for new listings"""
    url = "https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Add your parsing logic here
        print("Checked ImmobilienScout24")

def main():
    load_dotenv()
    
    # Schedule checks every 30 minutes
    schedule.every(30).minutes.do(check_immoscout24)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 