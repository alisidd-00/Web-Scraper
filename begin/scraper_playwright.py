import asyncio
import pandas as pd
import os
import random
from playwright.async_api import async_playwright

# List of proxies
proxies = [
    "http://114.156.77.107:8080",
    "http://20.111.54.16:8123",
    "http://113.160.132.195:8080",
    'http://43.200.77.128:3128',
    'http://83.68.136.236:80',
    'http://179.96.28.58:80',
    'http://198.44.255.5:80',
    'http://47.88.59.79:82',
    'http://51.254.78.223:80',
    'http://43.203.253.129:8004',
    'http://18.231.176.166:8363',
    # Add more proxies as needed
]

async def scrape_company_names(page):
    try:
        print("Navigating to the main page...")
        await page.goto('https://es.kompass.com/businessplace/z/de/', wait_until='networkidle', timeout=120000)

        # Wait for manual CAPTCHA solving
        print("Waiting for CAPTCHA to be solved...")
        await page.wait_for_selector('a.title', timeout=60000)  # Wait indefinitely for the title element to load

        # Scrape the company names
        print("Scraping company names...")
        companies = await page.query_selector_all('a.title')
        company_list = []

        for company in companies:
            await asyncio.sleep(random.uniform(2, 8))  # Increased delay

            company_name = await company.inner_text()
            print(f"Found company: {company_name}")
            company_list.append(company_name)

        return company_list
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

async def main():
    try:
        async with async_playwright() as p:
            print("Launching the browser...")
            browser = await p.chromium.launch(headless=False, args=['--no-sandbox', '--disable-setuid-sandbox'])

            for proxy in proxies:
                print(f"Using proxy: {proxy}")
                
                # Create a new context with proxy settings
                context = await browser.new_context(proxy={"server": proxy})
                page = await context.new_page()

                # Scrape company names
                names = await scrape_company_names(page)

                if names:  # If scraping was successful, exit loop
                    break

                await page.close()  # Close page if scraping fails
                await context.close()  # Close the context

            else:
                print("All proxies failed to retrieve company names.")

            if names:
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
