import scrapy


class BookItem(scrapy.Item):
    title = scrapy.Field()
    img = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
