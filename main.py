import asyncio
import argparse
from tqdm import tqdm
from playwright.async_api import async_playwright
from scrapers.mathom_scraper import MathomScraper
from scrapers.dracotienda_scraper import DracotiendaScraper
from scrapers.dungeonmarvels_scraper import DungeonMarvelsScraper
from generate_html import generate_html, update_x_image_path

SCRAPERS = {
    'mathom': MathomScraper,
    'dracotienda': DracotiendaScraper,
    'dungeonmarvels': DungeonMarvelsScraper
}


async def scrape_store(scraper_class, keyword, progress_bar):
    scraper = scraper_class()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the sales page
        await page.goto(scraper.url)

        # Ensure the page is fully loaded
        await page.wait_for_load_state('networkidle')

        # Get total items
        total_items = await scraper.get_total_items(page)

        # Scrape the sales page
        results = await scraper.scrape_sales_page(page, keyword, total_items, progress_bar)
        await browser.close()
    return results


async def main(keyword, store=None):
    results = []
    if store:
        if store not in SCRAPERS:
            print(f"Store '{store}' is not supported.")
            return
        scraper_class = SCRAPERS[store]
        with tqdm(total=1, desc="Scraping products", unit="store") as pbar:
            results.extend(await scrape_store(scraper_class, keyword, pbar))
    else:
        total_items = 0
        # Calculate total items across all stores for the progress bar
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            for scraper_class in SCRAPERS.values():
                scraper = scraper_class()
                await page.goto(scraper.url)
                await page.wait_for_load_state('networkidle')
                total_items += await scraper.get_total_items(page)
            await browser.close()

        with tqdm(total=total_items, desc="Scraping products", unit="item") as pbar:
            tasks = [scrape_store(scraper_class, keyword, pbar) for scraper_class in SCRAPERS.values()]
            all_results = await asyncio.gather(*tasks)
            for result in all_results:
                results.extend(result)

    # Sort results by discount percentage in descending order
    results.sort(key=lambda x: int(x['Rebaja'].rstrip('%')), reverse=True)

    # Generate HTML
    generate_html(results)

    # Update the placeholder for the 'X' image path
    x_image_path = 'x_image.png'
    update_x_image_path(x_image_path)

    print(f"Scraped total {len(results)} items.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape product sales from various e-commerce sites.')
    parser.add_argument('keyword', type=str, help='Keyword to filter product titles')
    parser.add_argument('--store', type=str,
                        help='The store to scrape (e.g., mathom, dracotienda, dungeonmarvels). Scrapes all stores if not specified.')
    args = parser.parse_args()

    asyncio.run(main(args.keyword, args.store))