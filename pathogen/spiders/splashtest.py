import scrapy
import json
from logging import debug
from ..common.mount_url import mount_url


class SplashtestSpider(scrapy.Spider):
    name = 'splashtest'
    
    start_urls = ['https://pathogen.watch/api/collection/summary?prefilter=all']

    def parse(self, response):
        # Default callback to process downloaded responses from
        # :param response response: return scrapped data from each URL
        
        # data variable receive page data 
        # from body HTML in str format.
        data = response.body
        
        # parse to JSON format
        parsed_json_data = json.loads(data)

        # loop responsable to pass for each collection page
        for collection in parsed_json_data['collections']:

        #     # URL variable receive each mountted collection URL
            url = mount_url(collection['token'])
            
            # Callback each processed collection
            # and return each scrapped collection
            # yield scrapy.Request(
            #     url=url,
            #     callback=self.parse_collection
            # )

            yield scrapy.Request(
                url=url,
                callback=self.parse_collection
            )

    def parse_collection(self, response):
        debug(response.txt)
        return response