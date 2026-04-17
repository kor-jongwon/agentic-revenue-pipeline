from .base_agent import BaseAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

class OracleAgent(BaseAgent):
    """
    The Oracle Agent: Responsible for data ingestion.
    Collects real-time financial data for IREN (Iris Energy) and AI infrastructure.
    """
    def __init__(self):
        super().__init__("Oracle Agent", "Data Ingestor")
        self.target_url = "https://www.google.com/finance/quote/IREN:NASDAQ"

    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # In a Docker environment, the binary location might be fixed
        # chrome_options.binary_location = "/usr/bin/google-chrome"
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def run(self):
        self.log(f"Starting detailed data collection from {self.target_url}")
        driver = None
        try:
            driver = self._setup_driver()
            driver.get(self.target_url)
            
            # Wait for price element to be visible
            # Google Finance price class usually starts with 'YMl54e' or similar, 
            # but let's use a more robust selector.
            wait = WebDriverWait(driver, 10)
            price_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class*="YMl54e"]')))
            
            price = price_element.text
            title = driver.title
            
            # Try to get percentage change
            try:
                change_element = driver.find_element(By.CSS_SELECTOR, 'div[class*="Jw7Xth"]')
                change = change_element.text
            except:
                change = "N/A"

            data = {
                "symbol": "IREN",
                "name": "Iris Energy Limited",
                "price": price,
                "change": change,
                "source": "Google Finance",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "status": "success"
            }
            
            self.log(f"Successfully collected data: {price} ({change})")
            return data

        except Exception as e:
            self.log(f"Error during collection: {str(e)}")
            return {
                "symbol": "IREN",
                "status": "error",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        finally:
            if driver:
                driver.quit()
