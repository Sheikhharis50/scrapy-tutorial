import os

# from pathlib import Path
from typing import Any

import scrapy
from scrapy.http.response.text import TextResponse

from .. import constants


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def __init__(self, name: str | None = None, **kwargs: Any):
        self.path = os.path.join(constants.OUTPUT_DIR, self.name)
        os.makedirs(self.path, exist_ok=True)
        super().__init__(name, **kwargs)

    def parse(self, response: TextResponse):
        # page = response.url.split("/")[-2]
        # filename = os.path.join(self.path, f"page-{page}.json")

        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        # self.log(f"Saved file {filename}")
