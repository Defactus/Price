import asyncio
from playwright.async_api import async_playwright
import urllib.parse
import re

async def get_shopee_price_with_retry(page, product_name):
    query = urllib.parse.quote(product_name)
    url = f"https://shopee.com.br/search?keyword={query}"
    try:
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(8000) # Wait a long time for shopee

        # Take a screenshot to see what Shopee is actually rendering
        await page.screenshot(path="shopee_debug.png")

        # Let's try to extract ALL text from the page to see if we see prices
        content = await page.content()
        with open("shopee_debug.html", "w") as f:
            f.write(content)

        print("Shopee screenshots and html saved")
    except Exception as e:
        print(f"Erro Shopee: {e}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
            ]
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = await context.new_page()
        await get_shopee_price_with_retry(page, "Smartphone Samsung Galaxy S23")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
