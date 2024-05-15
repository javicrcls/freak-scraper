# scrapers/mathom_scraper.py
from scrapers.base_scraper import BaseScraper
from tqdm import tqdm

class MathomScraper(BaseScraper):
    def __init__(self, url='https://mathom.es/en/2507-sales'):
        super().__init__(url)

    async def get_total_items(self, page):
        product_count = await page.query_selector('.product-count')
        product_count_text = await product_count.inner_text()
        total_items = int(product_count_text.split()[-2])
        return total_items

    async def scrape_sales_page(self, page, keyword, total_items):
        results = []
        products = await page.query_selector_all('li.ajax_block_product')
        with tqdm(total=total_items, desc="Scraping products", unit="product") as pbar:
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

                price = float(price_text.replace('€', '').replace(',', '').strip()) if price_text != 'N/A' else 0
                old_price = float(old_price_text.replace('€', '').replace(',', '').strip()) if old_price_text != 'N/A' else 0

                discount_percentage = 0
                if old_price > 0:
                    discount_percentage = round(((old_price - price) / old_price) * 100)

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