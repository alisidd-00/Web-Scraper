from playwright.sync_api import sync_playwright
import random
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of proxies
PROXIES = [
    'http://158.255.77.169:80',
    'http://43.200.77.128:3128',
    'http://83.68.136.236:80',
    'http://179.96.28.58:80',
    'http://198.44.255.5:80',
]

TARGET_URL = 'https://es.kompass.com/businessplace/z/de/'
DELAY_MIN = 3
DELAY_MAX = 5

def random_delay():
    """Introduce a random delay to mimic human behavior."""
    delay = random.uniform(DELAY_MIN, DELAY_MAX)
    logging.info(f"Waiting for {delay:.2f} seconds...")
    time.sleep(delay)

def scrape_company_name(page):
    """Scrape the company name from the page."""
    logging.info("Scraping the company name...")
    company = page.query_selector('a.title')
    if company:
        return company.inner_text()
    else:
        logging.warning("No company found.")
        return None

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        for proxy in PROXIES:
            logging.info(f"Using proxy: {proxy}")
            page = browser.new_page(proxy={"server": proxy})

            try:
                random_delay()  # Delay before navigation
                logging.info("Navigating to the target page...")
                page.goto(TARGET_URL, wait_until='networkidle', timeout=60000)
                
                random_delay()  # Delay after navigation

                # Allow user to solve CAPTCHA if prompted
                logging.info("Please solve the CAPTCHA manually if prompted...")
                random_delay()

                company_name = scrape_company_name(page)
                if company_name:
                    logging.info(f"Company Name: {company_name}")
                    break  # Exit loop if successful

            except Exception as e:
                logging.error(f"An error occurred with proxy {proxy}: {e}")

            finally:
                page.close()

        browser.close()
        logging.info("Browser closed.")

if __name__ == "__main__":
    main()
