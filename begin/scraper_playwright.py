import asyncio
import pandas as pd
import os
import random
from playwright.async_api import async_playwright

async def scrape_company_names(page):
    try:
        print("Navigating to the main page...")
        await page.goto('https://es.kompass.com/businessplace/z/de/', wait_until='networkidle', timeout=60000)

        # Wait for manual CAPTCHA solving
        print("Waiting for CAPTCHA to be solved...")
        await page.wait_for_selector('a.title', timeout=0)  # Wait indefinitely for the title element to load

        # Scrape the company names
        print("Scraping company names...")
        companies = await page.query_selector_all('a.title')  # Adjust the selector as needed
        company_list = []

        for company in companies:
            # Random delay to mimic human behavior
            await asyncio.sleep(random.uniform(1, 6))  # Sleep for 1 to 6 seconds

            company_name = await company.inner_text()  # Get the text content of each company element
            print(f"Found company: {company_name}")
            company_list.append(company_name)

        return company_list
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return []

async def main():
    try:
        async with async_playwright() as p:
            print("Launching the browser...")
            browser = await p.chromium.launch(headless=False)  # Show the browser window
            page = await browser.new_page()

            # Scrape company names
            names = await scrape_company_names(page)

            # Save names to CSV
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            csv_file_path = os.path.join(desktop_path, "company_names.csv")
            df = pd.DataFrame(names, columns=["Company Name"])
            df.to_csv(csv_file_path, index=False)
            print(f"Company names saved to {csv_file_path}")

            await browser.close()
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    asyncio.run(main())
