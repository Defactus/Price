import asyncio
from playwright.async_api import async_playwright
import urllib.parse

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        product_name = "Smartphone Samsung Galaxy S23"
        query = urllib.parse.quote(product_name)
        url = f"https://lista.mercadolivre.com.br/{query}"

        print(f"Acessando: {url}")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Tirar um screenshot para ver o que carregou
        await page.screenshot(path="ml_debug.png")
        print("Screenshot salvo como ml_debug.png")

        content = await page.content()
        with open("ml_debug.html", "w") as f:
            f.write(content)

        print("HTML salvo como ml_debug.html")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
