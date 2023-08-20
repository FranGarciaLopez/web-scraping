import scrapy
import json
from scrapy.crawler import CrawlerProcess

class AnimeSpider(scrapy.Spider):
          name = 'anime_spider'
          start_urls = ['https://www3.animeflv.net/browse']
          allowed_domains = ['animeflv.net']
    custom_settings = {
            'LOG_LEVEL': logging.INFO 
    }

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
class TestAnimeSpider(unittest.TestCase):

    def setUp(self):
        self.mock_response = HtmlResponse(url='https://www3.animeflv.net/browse', body=b'<html><body><h3 class="Title">Title 1</h3><h3 class="Title">Title 2</h3></body></html>')

    def test_parse_function(self):
        spider = AnimeSpider()
        parsed_items = list(spider.parse(self.mock_response))
        expected_items = [{'title': 'Title 1'}, {'title': 'Title 2'}]
        self.assertEqual(parsed_items, expected_items)

    def test_next_page_navigation(self):
        spider = AnimeSpider()
        with patch('scrapy.http.HtmlResponse.css') as mock_css:
            mock_css.return_value.get.return_value = '/next-page'
            next_page_request = next(spider.parse(self.mock_response))
            self.assertEqual(next_page_request.url, 'https://www3.animeflv.net/next-page')
            self.assertEqual(next_page_request.callback, spider.parse)

          def close_spider(self, spider):
                    with open('data.json', 'w') as f:
                              json.dump(self.items, f, indent=2)

process = CrawlerProcess(settings={
    'ITEM_PIPELINES': {'__main__.SaveToJsonPipeline': 1},
})

process.crawl(AnimeSpider)
process.start()