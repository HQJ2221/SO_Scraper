import scrapy

class StackoverflowScraperItem(scrapy.Item):
    title = scrapy.Field()
    votes = scrapy.Field()
    views = scrapy.Field()
    answers = scrapy.Field()
    link = scrapy.Field()
    problems = scrapy.Field()  # 添加问题描述字段
    solutions = scrapy.Field()  # 添加答案字段
