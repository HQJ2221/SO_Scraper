import scrapy

class StackoverflowScraperItem(scrapy.Item):
    title = scrapy.Field()
    votes = scrapy.Field()
    views = scrapy.Field()
    answers = scrapy.Field()
    link = scrapy.Field()
