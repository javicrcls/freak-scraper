from scrapers.base_scraper import BaseScraper
from tqdm import tqdm

class DungeonMarvelsScraper(BaseScraper):
    def __init__(self, url='https://dungeonmarvels.com/217-super-ofertas?q=Disponibilidad-En+stock'):
        super().__init__(url)

    async def get_total_items(self, page):
        product_count = await page.query_selector('div.total-products p')
        product_count_text = await product_count.inner_text()
        total_items = int(product_count_text.split()[1])
        return total_items

    async def get_total_pages(self, page):
        pagination_elements = await page.query_selector_all('ul.page-list li a:not([rel="next"])')
        last_page_number = 1
        for element in pagination_elements:
            page_number_text = await element.inner_text()
            if page_number_text.isdigit():
                last_page_number = max(last_page_number, int(page_number_text))
        return last_page_number

    async def scrape_sales_page(self, page, keyword, total_items):
        results = []
        total_pages = await self.get_total_pages(page)

        with tqdm(total=total_items, desc="Scraping products", unit="product") as pbar:
            for current_page in range(1, total_pages + 1):
                await page.goto(f'{self.url}&page={current_page}')
                await page.wait_for_load_state('networkidle')
                products = await page.query_selector_all('div#js-product-list article.product-miniature')

                for product in products:
                    availability = await product.query_selector('div.stock-product span.stock-tag')
                    availability_text = await availability.inner_text() if availability else 'N/A'
                    if 'Reserva' in availability_text:
                        continue

                    title_element = await product.query_selector('h2.product-title a')
                    price_element = await product.query_selector('div.product-price-and-shipping span.price')
                    old_price_element = await product.query_selector('div.product-price-and-shipping span.regular-price')
                    image_element = await product.query_selector('div.thumbnail-container img')

                    title = await title_element.inner_text() if title_element else 'N/A'
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