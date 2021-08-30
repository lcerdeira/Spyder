import scrapy
import json
from scrapy_selenium import SeleniumRequest
from logging import debug

from ..common.mount_url import mount_url


class ScrapyseleniumSpider(scrapy.Spider):
    name = 'scrapyselenium'
    start_urls = ['https://pathogen.watch/api/collection/summary?prefilter=all']

    def parse(self, response):
        data = response.body
        
        # parse to JSON format
        parsed_json_data = json.loads(data)

        parsed_json_data['summary']['organismId']

        # loop responsable to pass for each collection page
        for collection in parsed_json_data['collections']:

        #     # URL variable receive each mountted collection URL
            url = mount_url(collection['token'])
            
            # Callback each processed collection
            # and return each scrapped collection
            yield SeleniumRequest(
                url=url,
                wait_time=10,
                callback=self.parse_collection
            )

    def parse_collection(self, response):
        debug(response.xpath('//body').extract())