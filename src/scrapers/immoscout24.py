import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

class ImmoscoutScraper:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://www.immobilienscout24.de"
        self.max_price = float(os.getenv('MAX_PRICE', 2000))
        self.min_rooms = float(os.getenv('MIN_ROOMS', 2))
        self.preferred_areas = os.getenv('PREFERRED_AREAS', '["Berlin"]')

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def get_listings(self):
        driver = self.setup_driver()
        listings = []
        
        try:
            # Construct search URL with filters
            search_url = f"{self.base_url}/Suche/de/berlin/berlin/wohnung-mieten?price=-{self.max_price}&rooms={self.min_rooms}"
            driver.get(search_url)
            
            # Wait for listings to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "result-list__listing"))
            )
            
            # Extract listings
            listing_elements = driver.find_elements(By.CLASS_NAME, "result-list__listing")
            
            for element in listing_elements[:10]:  # Limit to first 10 results
                try:
                    listing = {
                        'id': element.get_attribute('data-id'),
                        'price': self.extract_price(element),
                        'size': self.extract_size(element),
                        'rooms': self.extract_rooms(element),
                        'location': self.extract_location(element),
                        'description': self.extract_description(element),
                        'url': self.extract_url(element),
                        'source': 'ImmobilienScout24'
                    }
                    listings.append(listing)
                except Exception as e:
                    print(f"Error extracting listing: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping ImmobilienScout24: {str(e)}")
        finally:
            driver.quit()
            
        return listings

    def extract_price(self, element):
        try:
            price_element = element.find_element(By.CLASS_NAME, "result-list-entry__criteria-item-price")
            return float(price_element.text.replace('€', '').replace('.', '').strip())
        except:
            return None

    def extract_size(self, element):
        try:
            size_element = element.find_element(By.CLASS_NAME, "result-list-entry__criteria-item-size")
            return float(size_element.text.replace('m²', '').strip())
        except:
            return None

    def extract_rooms(self, element):
        try:
            rooms_element = element.find_element(By.CLASS_NAME, "result-list-entry__criteria-item-rooms")
            return float(rooms_element.text.strip())
        except:
            return None

    def extract_location(self, element):
        try:
            location_element = element.find_element(By.CLASS_NAME, "result-list-entry__address")
            return location_element.text.strip()
        except:
            return None

    def extract_description(self, element):
        try:
            desc_element = element.find_element(By.CLASS_NAME, "result-list-entry__title")
            return desc_element.text.strip()
        except:
            return None

    def extract_url(self, element):
        try:
            url_element = element.find_element(By.CLASS_NAME, "result-list-entry__brand-title-container")
            return url_element.get_attribute('href')
        except:
            return None 