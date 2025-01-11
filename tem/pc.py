import scrapy
import time
from stackoverflow_scraper.items import StackoverflowScraperItem

class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    allowed_domains = ['stackoverflow.com']

    def __init__(self):
        self.count = 1
        self.page_count = 0  # 用于计数每次爬取的页数

    def start_requests(self):
        _url = 'https://stackoverflow.com/questions/tagged/opencv?page={page}&sort=votes&pagesize=50'
        urls = [_url.format(page=page) for page in range(31, 1400)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for question in response.xpath('//*[@id="questions"]/div'):
            self.count += 1

            item = StackoverflowScraperItem()

            # 使用新的XPath提取投票数、标题和链接
            item['votes'] = question.xpath('.//span[@class="vote-count-post "]/strong/text()').get(default="0")
            item['title'] = question.xpath('.//h3/a/text()').get(default="N/A")
            relative_link = question.xpath('.//h3/a/@href').get(default="")
            item['link'] = response.urljoin(relative_link)

            # 设置文件路径为项目目录下的 output 文件夹
            filepath = f"./output/{self.count - 1}.txt"
            with open(filepath, "w") as f:
                f.write(str(item))

            yield item

        # 每爬取30页后休息15秒
        self.page_count += 1
        if self.page_count % 30 == 0:
            self.log("Pausing for 15 seconds...")
            time.sleep(15)
