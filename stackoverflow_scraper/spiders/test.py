import scrapy
from stackoverflow_scraper.items import StackoverflowScraperItem
from time import sleep

class StackoverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    allowed_domains = ['stackoverflow.com']

    def start_requests(self):
        # 逐个获取文件路径，尝试读取URL
        for num in range(1, 68364):  # 从1到68363个文件
            filepath = f"./output/{num}.txt"
            
            try:
                with open(filepath, "r") as f:
                    # 按行读取，找到包含'link'的行并提取URL
                    for line in f:
                        if "'link':" in line:
                            url = line.split("'")[3]  # 提取URL
                            break
                    else:
                        self.log(f"URL not found in {filepath}")
                        continue  # 如果找不到URL，则跳过

                    # 爬取减速，避免被反爬
                    yield scrapy.Request(url=url, callback=lambda response, number=num: self.parse(response, number), dont_filter=True)

            except FileNotFoundError:
                self.log(f"File {filepath} not found. Skipping this entry.")
            
            # 每读取30个文件，休息5秒
            if num % 15 == 0:
                self.log("Pausing for 5 seconds to avoid rate limiting...")
                sleep(8)

    def parse(self, response, number):
        item = StackoverflowScraperItem()
        
        # 提取问题描述
        sel1 = response.xpath('//*[@id="question"]//div[@class="s-prose js-post-body"]')
        item['problems'] = sel1.xpath('string(.)').get(default="没有找到问题描述")

        # 提取多个回答
        solutions = []
        sel2s = response.xpath('//*[@id="answers"]//div[@class="s-prose js-post-body"]')
        for sel in sel2s:
            solutions.append(sel.xpath('string(.)').get())

        # 使用分隔符拼接回答
        item['solutions'] = "............................................................".join(solutions)

        # 写入到对应的文件
        filepath = f"./qa/{number}.txt"
        with open(filepath, "a", encoding='utf-8') as f:
            f.write("\n")
            f.write(str(item))

        yield item
