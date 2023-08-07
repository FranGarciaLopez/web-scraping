import scrapy
import json
from scrapy.crawler import CrawlerProcess

class AnimeSpider(scrapy.Spider):
          name = 'anime_spider'
          start_urls = ['https://www3.animeflv.net/browse']
          allowed_domains = ['animeflv.net']

          def parse(self, response):
          
                    titles = response.css('h3.Title::text').extract()
                    titles = [title.strip() for title in titles if title.strip()]

                    # Yield the titles
                    for title in titles:
                              yield {'title': title}

          
                    next_page = response.css('li.active + li a::attr(href)').get()
                    if next_page:
                              yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)


class SaveToJsonPipeline:
          def __init__(self):
                    self.items = []

          def process_item(self, item, spider):
                    self.items.append(item)
                    return item

          def close_spider(self, spider):
                    with open('data.json', 'w') as f:
                              json.dump(self.items, f, indent=2)

process = CrawlerProcess(settings={
    'ITEM_PIPELINES': {'__main__.SaveToJsonPipeline': 1},
})

process.crawl(AnimeSpider)
process.start()