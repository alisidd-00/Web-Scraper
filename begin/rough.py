import asyncio
from playwright.async_api import async_playwright

async def fetch_proxies(page):
    try:
        await page.goto("https://free-proxy-list.net/", wait_until='networkidle', timeout=60000)

        # Check the full page content to debug
        content = await page.content()
        print("Full Page content loaded for debugging:")
        print(content)  # Print the entire page content

        # Scrape the proxy table
        print("Fetching proxies...")
        rows = await page.query_selector_all('table#proxylisttable tbody tr')
        proxies = []

        for row in rows:
            columns = await row.query_selector_all('td')
            if len(columns) >= 2:  # Ensure there are at least two columns for IP and port
                ip = await columns[0].inner_text()
                port = await columns[1].inner_text()
                proxies.append(f"{ip}:{port}")

        print(f"Fetched {len(proxies)} proxies.")
        return proxies

    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

async def main():
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=False)  # Show the browser window
        context = await browser.new_context()  # Create a new context for the scraping

        page = await context.new_page()

        # Fetch proxies
        proxies = await fetch_proxies(page)

        # Output proxies to verify
        print("Proxies fetched:", proxies)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
