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


