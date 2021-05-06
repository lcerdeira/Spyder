import scrapy
import json
from ..common.save_csv_file import save_csv_file
from ..common.mount_url import mount_url
from ..common.organisms import organisms


class CollectionsSpider(scrapy.Spider):
    # Spider responsable for collection csv data 
    # by forms from page

    # spider`s name
    name = 'collections' 

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

        # init ids array variable
        ids = []

        # init separator str variable
        separator = ','

        # loop responsable to pass for each id 
        # on genomes property and push to ids array
        for genome in parsed_json_data['genomes']:
            ids.append(genome['id'])
        
        # genome_ids variable receive amount of ids 
        # to pass by form submit
        genome_ids = separator.join(ids)

        # form_data variable receive mountted params in JSON format
        form_data = {
            'ids': genome_ids
        }

        # token variable receive token identification from page data
        token = parsed_json_data['token']

        # loop responsable for take each organism and token to correct collection`s URL
        for organism_name, organism_id in organisms():
            # check if on correct organism
            if organism_id == parsed_json_data['organismId']:
                # urls list variable
                urls = [
                    f'https://pathogen.watch/download/collection/{token}/speciator?filename=pathogenwatch-{organism_name}-{token}-species-prediction.csv',
                    f'https://pathogen.watch/download/collection/{token}/kleborate?filename=pathogenwatch-{organism_name}-{token}-kleborate.csv',
                    f'https://pathogen.watch/download/collection/{token}/core-allele-distribution?filename=pathogenwatch-{organism_name}-{token}-core-allele-distribution.csv',
                    f'https://pathogen.watch/download/collection/{token}/score-matrix?filename=pathogenwatch-{organism_name}-{token}-score-matrix.csv',
                    f'https://pathogen.watch/download/collection/{token}/difference-matrix?filename=pathogenwatch-{organism_name}-{token}-difference-matrix.csv'
                ]

                # loop responsable to submit each data created by form_data variable
                # to correct collection`s URL 
                # and by pass token (collection identification) args & organism name
                for url in urls:
                    yield scrapy.FormRequest(
                        url=url,
                        method='POST',
                        formdata=form_data,
                        callback=save_csv_file,
                        cb_kwargs=dict(token=token, organism=organism_name)
                    )
