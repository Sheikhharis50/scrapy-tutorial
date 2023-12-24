import scrapy
from scrapy.http.response.text import TextResponse
from scrapy.selector import Selector

from app.items.book import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}  # Ignore the robots.txt file

    def parse(self, response: TextResponse):
        books = response.css("article.product_pod")
        self.logger.info(f"books found: {len(books)}")

        def extract(selector: Selector, query: str, clean=None) -> str | None:
            result = selector.css(query).get()
            self.logger.info("result: %s", result)
            if result and type(result) == str:
                result = result.strip()
            if clean:
                result = clean(result)
            return result

        for book in books:
            item = BookItem()
            item["title"] = extract(book, "h3 a::attr(title)")
            item["img"] = extract(book, "div.image_container img::attr(src)")
            item["url"] = extract(book, "div.image_container a::attr(href)")
            item["price"] = extract(book, "div.product_price p.price_color::text")
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
