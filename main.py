import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# Initialize the user agent generator
user_agent = UserAgent()

# Set up Chrome options with random user agent
def init_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Helps avoid detection
    options.add_argument(f"user-agent={user_agent.random}")  # Set a random user agent

    # Optional: run in headless mode (uncomment to see actions visually)
    # options.add_argument("--headless")

    # Initialize WebDriver with the above options
    driver = webdriver.Chrome(options=options)
    return driver

# Mimic human behavior with a delay function
def human_delay():
    time.sleep(random.uniform(1, 3))

# Example scraping function
def scrape_page():
    driver = init_driver()

    try:
        # Open the target webpage
        driver.get("https://es.kompass.com/businessplace/z/de/")
        human_delay()  # Simulate thinking time

        # Check if page loaded successfully by inspecting page title
        page_title = driver.title
        print("Page Title:", page_title)

        # Confirming success by checking if title is not empty
        if page_title:
            print("Connection successful: Page accessed.")
        else:
            print("Warning: Page title is empty; check if page loaded fully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the browser session
        driver.quit()

# Run the scraping function
scrape_page()
