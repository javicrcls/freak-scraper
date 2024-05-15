from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    async def get_total_items(self, page):
        pass

    @abstractmethod
    async def scrape_sales_page(self, page, keyword, total_items, progress_bar):
        pass