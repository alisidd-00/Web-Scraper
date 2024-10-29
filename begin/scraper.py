import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to scrape data from a company page
def scrape_company_data(driver, company_url):
    try:
        driver.get(company_url)
        time.sleep(random.uniform(2, 4))  # Wait for the page to load
        
        name = driver.find_element(By.CSS_SELECTOR, 'h2 span.titleSpan').text if driver.find_elements(By.CSS_SELECTOR, 'h2 span.titleSpan') else 'Not Available'
        phone = driver.find_element(By.CSS_SELECTOR, 'a.phone').text if driver.find_elements(By.CSS_SELECTOR, 'a.phone') else 'Not Available'
        email = driver.find_element(By.CSS_SELECTOR, 'a.email').text if driver.find_elements(By.CSS_SELECTOR, 'a.email') else 'Not Available'

        return {
            'Name': name,
            'Phone': phone,
            'Email': email
        }
    except Exception as e:
        print(f"Error while scraping {company_url}: {e}")
        return {
            'Name': 'Not Available',
            'Phone': 'Not Available',
            'Email': 'Not Available'
        }

# Main function to scrape the main page
def main():
    # Setup Brave options
    options = Options()
    options.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'  # Adjust this path if necessary
    
    # Add proxy settings
    proxy = "http://85.172.5.74	3629"  # Your provided proxy address
    options.add_argument(f'--proxy-server={proxy}')

    # Setup Selenium WebDriver with Brave
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    base_url = "https://es.kompass.com/businessplace/z/de/"
    company_data_list = []

    try:
        driver.get(base_url)
        time.sleep(random.uniform(2, 4))  # Wait for the page to load

        # Extract company links
        company_links = driver.find_elements(By.CSS_SELECTOR, 'a.company-link')

        for link in company_links:
            company_url = link.get_attribute('href')
            company_data = scrape_company_data(driver, company_url)
            company_data_list.append(company_data)

            time.sleep(random.uniform(1, 3))

        # Save data to CSV
        df = pd.DataFrame(company_data_list)
        df.to_csv('company_data.csv', index=False)

    except Exception as e:
        print(f"Error while accessing {base_url}: {e}")

    finally:
        driver.quit()  # Close the browser

if __name__ == "__main__":
    main()
