from scrapers.base_scraper import BaseScraper

class DracotiendaScraper(BaseScraper):
    def __init__(self, url='https://dracotienda.com/1879-ofertas'):
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

    async def scrape_sales_page(self, page, keyword, total_items, progress_bar):
        results = []
        total_pages = await self.get_total_pages(page)
        total_scraped = 0

        for current_page in range(1, total_pages + 1):
            await page.goto(f'{self.url}?page={current_page}')
            await page.wait_for_load_state('networkidle')
            products = await page.query_selector_all('section#products div.item')

            for product in products:
                title_element = await product.query_selector('h2.productName a')
                price_element = await product.query_selector('div.laber-product-price-and-shipping span.price')
                old_price_element = await product.query_selector('div.laber-product-price-and-shipping span.regular-price')
                image_element = await product.query_selector('div.laberProduct-image img')

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
                progress_bar.update(1)
        return results