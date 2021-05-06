import scrapy
import json
from ..common.mount_url import mount_url
from ..common.organisms import organisms
from ..common.save_nwk_file import save_nwk_file
from ..common.save_csv_file import save_csv_file


class CollectionsFromLinkSpider(scrapy.Spider):
    # Spider responsable fro collection csv and nwk 
    # by link and newick

    # spider`s name
    name = 'collections_from_link'

    # A list of URLs where the spider will begin crawlling from
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

            # URL variable receive each mountted collection URL
            url = mount_url(collection['token'])

            # Callback each processed collection
            # and return each scrapped collection
            yield scrapy.Request(
                url=url,
                callback=self.parse_collection
            )

    def parse_collection(self, response):
        # Get source collection page to filter
        # :param response response: return scrapped data from collection page

        # data variable receive page data 
        # from body HTML in str format.
        data = response.body

        # parse to JSON format
        parsed_json_data = json.loads(data)

        # token variable receive token identification from page data
        token = parsed_json_data['token']

        # tree variable receive newick data
        tree = parsed_json_data['tree']['newick']

        # debug point 
        # newick data
        # self.log(f'TREE ===>>> {tree}')

        # loop responsable for take each organism and token to correct collection`s URL 
        # and save newick file to each collection
        for organism_name, organism_id in organisms():
            # check if on correct organism
            if organism_id == parsed_json_data['organismId']:
                # save each newick file
                save_nwk_file(response, token, tree, organism_name)

                # url variable receive mountted correct collection`s URL
                url = f'https://pathogen.watch/download/collection/{token}/variance-summary?filename=pathogenwatch-{organism_name}-{token}-variance-summary.csv'

                # It is responsable for request each collection`s URL 
                # and callback saving csv
                # and by pass token (collection identification) args
                yield scrapy.Request(
                    url=url,
                    callback=save_csv_file,
                    cb_kwargs=dict(token=token, organism=organism_name)
                )

