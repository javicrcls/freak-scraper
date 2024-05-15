import asyncio
import argparse
from tqdm import tqdm
from playwright.async_api import async_playwright
from generate_html import generate_html, update_x_image_path


async def scrape_sales_page(page, keyword, total_items):
    # Extract product details
    results = []
    # Create a progress bar for scraping products
    with tqdm(total=total_items, desc="Scraping site", unit="product") as pbar:
        products = await page.query_selector_all('li.ajax_block_product')
        for product in products:
            title_element = await product.query_selector('h5.s_title_block a.product-name')
            price_element = await product.query_selector('.price_container .price.product-price')
            old_price_element = await product.query_selector('.price_container .old-price.product-price')
            image_element = await product.query_selector('img.front-image')

            title = await title_element.get_attribute('title') if title_element else 'N/A'
            href = await title_element.get_attribute('href') if title_element else 'N/A'
            price_text = await price_element.inner_text() if price_element else 'N/A'
            old_price_text = await old_price_element.inner_text() if old_price_element else 'N/A'
            image_url = await image_element.get_attribute('src') if image_element else ''

            # Remove currency symbols and commas to convert to float
            price = float(price_text.replace('€', '').replace(',', '').strip()) if price_text != 'N/A' else 0
            old_price = float(
                old_price_text.replace('€', '').replace(',', '').strip()) if old_price_text != 'N/A' else 0

            # Calculate discount percentage
            discount_percentage = 0
            if old_price > 0:
                discount_percentage = round(((old_price - price) / old_price) * 100)

            # Filter based on the keyword
            if keyword.lower() in title.lower():
                results.append({
                    'Producto': title,
                    'Enlace': href,
                    'Precio': price_text,
                    'Precio sin descuento': old_price_text,
                    'Rebaja': f"{discount_percentage}%",
                    'Imagen': image_url
                })
            pbar.update(1)
    return results


async def main(keyword):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set to True for headless mode
        page = await browser.new_page()

        # Directly navigate to the sales page
        await page.goto('https://mathom.es/en/2507-sales')

        # Ensure the page is fully loaded
        await page.wait_for_load_state('networkidle')

        # Extract the number of items from the product count div
        print("Getting total sale items...")
        product_count = await page.query_selector('.product-count')
        product_count_text = await product_count.inner_text()
        total_items = int(product_count_text.split()[-2])
        print(f"Total sale items: {total_items}")

        # Navigate to the URL showing all items on a single page
        await page.goto(f'https://mathom.es/en/2507-sales?id_category=2507&n={total_items}')

        # Ensure the page is fully loaded
        await page.wait_for_load_state('networkidle')

        # Scrape the sales page
        results = await scrape_sales_page(page, keyword, total_items)

        # Sort results by discount percentage in descending order
        results.sort(key=lambda x: int(x['Rebaja'].rstrip('%')), reverse=True)

        # Generate HTML
        generate_html(results)

        # Update the placeholder for the 'X' image path
        x_image_path = 'x_image.png'  # Update this path to the actual path of the 'X' image
        update_x_image_path(x_image_path)

        print(f"Scraped total {len(results)} items.")
        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape product sales from mathom.es.')
    parser.add_argument('keyword', type=str, help='Keyword to filter product titles')
    args = parser.parse_args()

    asyncio.run(main(args.keyword))