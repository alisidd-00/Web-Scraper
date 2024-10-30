import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_company_data(page, company_url):
    await page.goto(company_url)
    await page.wait_for_timeout(3000)  # Wait for content to load

    # Scrape data
    name = await page.inner_text('h2 span.titleSpan') or 'Not Available'
    phone = await page.inner_text('a.phone') or 'Not Available'
    email = await page.inner_text('a.email') or 'Not Available'

    return {
        'Name': name,
        'Phone': phone,
        'Email': email
    }

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://es.kompass.com/businessplace/z/de/')
        await page.wait_for_timeout(3000)  # Wait for content to load

        # Scrape company links
        company_links = await page.query_selector_all('a.company-link')
        company_data_list = []

        for link in company_links:
            company_url = await link.get_attribute('href')
            print(f"Scraping data from {company_url}...")
            company_data = await scrape_company_data(page, company_url)
            company_data_list.append(company_data)

        # Save data to CSV
        df = pd.DataFrame(company_data_list)
        df.to_csv('company_data.csv', index=False)
        print("Data saved to company_data.csv")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
